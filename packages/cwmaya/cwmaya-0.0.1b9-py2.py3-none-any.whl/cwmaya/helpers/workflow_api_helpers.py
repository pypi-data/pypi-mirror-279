import pymel.core as pm
import os
import json

import requests

from cwmaya.helpers import const as k
from cwmaya.windows import window_utils
from cwmaya.windows import jobs_index
from ciocore import data as coredata

from contextlib import contextmanager


@contextmanager
def save_scene():
    """
    A context manager to save the current scene before executing the block of code.

    Yields:
        None: Yields control back to the context block after saving the scene.

    Usage Example:
    ```
    with save_scene():
        # Perform actions that require the scene to be saved
    ```
    """
    try:
        if pm.isModified():
            filters = "Maya Files (*.ma *.mb);;Maya ASCII (*.ma);;Maya Binary (*.mb);;All Files (*.*)"
            entries = pm.fileDialog2(
                caption="Save File As",
                okCaption="Save As",
                fileFilter=filters,
                dialogStyle=2,
                fileMode=0,
                dir=os.path.dirname(pm.sceneName()),
            )
            if entries:
                filepath = entries[0]
                pm.saveAs(filepath)
        yield
    except Exception as err:
        pm.displayError(str(err))
    finally:
        pass


##### WORKFLOW API DISPLAY FUNCTIONS #####
def validate_job(node):
    try:
        response = request_validate_job(node)
        data = {"status_code": response.status_code, "text": response.text}
    except Exception as err:
        data = {"error": str(err)}
    window_utils.show_data_in_window(data, title="Workflow API | Validate job")


def health_check():
    try:
        response = request_health_check()
        data = {"status_code": response.status_code, "text": response.text}
    except Exception as err:
        data = {"error": str(err)}
    window_utils.show_data_in_window(data, title="Workflow API | Health check")


def list_jobs():
    try:
        response = request_list_jobs()

        # Check if the status code is an error code (4xx or 5xx)
        if response.status_code > 201:
            # You can raise a built-in HTTPError or define your own exception
            raise Exception(f"Error response {response.status_code}: {response.text}")

        data = json.loads(response.text)
    except Exception as err:
        data = {"error": str(err)}

    win = jobs_index.JobsIndex()
    win.hydrate(data)


def show_job(job):
    response = request_get_job(job["id"])
    try:
        if response.status_code > 201:
            raise Exception(f"Error response {response.status_code}: {response.text}")
        data = json.loads(response.text)
    except Exception as err:
        data = {"error": str(err)}

    window_utils.show_data_in_window(data, title="Workflow API | Show Job")


def show_nodes(job):
    response = request_get_nodes(job["id"])
    try:
        if response.status_code > 201:
            raise Exception(f"Error response {response.status_code}: {response.text}")
        data = json.loads(response.text)
    except Exception as err:
        data = {"error": str(err)}

    window_utils.show_data_in_window(data, title="Workflow API | Show Nodes")


def show_nodes_in_vscode(job):
    response = request_get_nodes(job["id"])
    try:
        if response.status_code > 201:
            raise Exception(f"Error response {response.status_code}: {response.text}")
        data = json.loads(response.text)
    except Exception as err:
        data = {"error": str(err)}

    window_utils.show_in_vscode(data)


def submit(node):
    if not node:
        print("No node found")
        return

    with save_scene():
        response = request_submit(node)
        response_data = json.loads(response.text)
        window_utils.show_data_in_window(response_data, title="Submission response")


def request_submit(node):
    headers = {"Content-Type": "application/json"}
    out_attr = node.attr("output")
    pm.dgdirty(out_attr)
    payload = out_attr.get()

    account_id = coredata.data()["account"]["account_id"]
    token = coredata.data()["account"]["token"]
    url = k.WORKFLOW_URLS["ACCOUNTS"]
    url = f"{url}/{account_id}/workflows"

    headers = {"Content-Type": "application/json", "Authorization": f"Bearer {token}"}

    return requests.post(url, data=payload, headers=headers, timeout=5)


def monitor_job(job):
    pass


##### WORKFLOW API REQUESTS #####
def request_health_check():
    url = k.WORKFLOW_URLS["HEALTHZ"]
    headers = {"Content-Type": "application/json"}
    return requests.get(url, headers=headers, timeout=5)


def request_list_jobs():
    account_id = coredata.data()["account"]["account_id"]
    token = coredata.data()["account"]["token"]
    url = k.WORKFLOW_URLS["ACCOUNTS"]
    url = f"{url}/{account_id}/workflows"
    headers = {"Content-Type": "application/json", "Authorization": f"Bearer {token}"}
    return requests.get(url, headers=headers, timeout=5)


def request_get_job(id):
    account_id = coredata.data()["account"]["account_id"]
    token = coredata.data()["account"]["token"]
    url = k.WORKFLOW_URLS["ACCOUNTS"]
    url = f"{url}/{account_id}/workflows/{id}"
    print("URL:", url)
    headers = {"Content-Type": "application/json", "Authorization": f"Bearer {token}"}
    return requests.get(url, headers=headers, timeout=5)


def request_get_nodes(id):
    account_id = coredata.data()["account"]["account_id"]
    token = coredata.data()["account"]["token"]
    url = k.WORKFLOW_URLS["ACCOUNTS"]
    url = f"{url}/{account_id}/workflows/{id}/nodes"
    print("URL:", url)
    headers = {"Content-Type": "application/json", "Authorization": f"Bearer {token}"}
    return requests.get(url, headers=headers, timeout=5)


def request_validate_job(node):
    headers = {"Content-Type": "application/json"}
    out_attr = node.attr("output")

    pm.dgdirty(out_attr)
    payload = out_attr.get()
    token = coredata.data()["account"]["token"]
    url = k.WORKFLOW_URLS["VALIDATE"]
    headers = {"Content-Type": "application/json", "Authorization": f"Bearer {token}"}
    return requests.post(url, data=payload, headers=headers, timeout=5)
