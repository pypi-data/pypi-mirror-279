import pymel.core as pm
from cwmaya.windows import window_utils

import requests
import json
from cwmaya.helpers import const as k
from ciocore import data as coredata
from contextlib import contextmanager


@contextmanager
def desktop_app(auth=False):
    """
    A context manager to check the health of the desktop application and optionally authenticate it.

    Yields:
        None: Yields control back to the context block if the health check succeeds (and authentication, if applicable).

    Parameters:
    - auth (bool): A flag to indicate whether authentication should be performed after the health check. Defaults to False.

    Usage Example:
    ```
    with desktop_app(auth=True):
        # Perform actions when the desktop app is healthy and authenticated
    ```

    If the health check or authentication fails, a window is displayed with the response or error message using `window_utils.show_data_in_window`.
    """
    errors = None
    try:
        response = request_health_check()
        if response.ok:
            if auth:
                auth_response = request_authenticate()
                if not auth_response.ok:
                    raise Exception(auth_response.text)
            yield auth_response
        else:
            errors = {"status_code": response.status_code, "text": response.text}
    except Exception as err:
        errors = {"error": str(err)}
    finally:
        if errors:
            window_utils.show_data_in_window(errors, title="Desktop app status")


# PUBLIC DISPLAY FUNCTIONS
def health_check():
    try:
        response = request_health_check()
        data = {"status_code": response.status_code, "text": response.text}
    except Exception as err:
        data = {"error": str(err)}
    window_utils.show_data_in_window(data, title="Desktop app health check")


def authenticate():
    with desktop_app(auth=True) as response:
        try:
            response.raise_for_status()
            data = {"status_code": response.status_code, "text": response.text}
        except Exception as err:
            data = {"error": str(err)}
        window_utils.show_data_in_window(data, title="Desktop app | Auth")


def navigate(route):
    response = request_navigate_graph(route)
    if response.status_code == 200:
        print(f"Successfully navigated to {route}")
    else:
        pm.error(f"Error navigating to {route}: {response.text}")


def send_to_composer(node):
    if not node:
        print("No node found")
        return
    with desktop_app(auth=True):
        url = k.DESKTOP_URLS["COMPOSER"]
        headers = {"Content-Type": "application/json"}
        out_attr = node.attr("output")
        pm.dgdirty(out_attr)
        payload = out_attr.get()
        response = requests.post(url, data=payload, headers=headers, timeout=5)
        if response.status_code == 200:
            print("Successfully sent payload to composer")
        else:
            pm.error("Error sending payload to composer:", response.text)


##### DESKTOP APP REQUESTS #####
def request_health_check():
    url = k.DESKTOP_URLS["HEALTHZ"]
    headers = {"Content-Type": "application/json"}
    return requests.get(url, headers=headers, timeout=5)


def request_authenticate():
    token = coredata.data()["account"]["token"]
    url = k.DESKTOP_URLS["AUTH"]
    headers = {"Content-Type": "application/json"}
    return requests.post(
        url, data=json.dumps({"token": token}), headers=headers, timeout=5
    )


def request_navigate_graph(route):
    if not route.startswith("/"):
        route = f"/{route}"

    url = k.DESKTOP_URLS["NAVIGATE"]
    data = json.dumps({"to": route})
    headers = {"Content-Type": "application/json"}
    return requests.post(url, data=data, headers=headers, timeout=5)


###############
