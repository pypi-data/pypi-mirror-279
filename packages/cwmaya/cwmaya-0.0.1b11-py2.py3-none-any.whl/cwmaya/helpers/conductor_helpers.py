import pymel.core as pm
from cwmaya.helpers import const as k
from ciocore import data as coredata


def hydrate_coredata(dialog, force=False):
    """
    Initializes core data with predefined services and attempts to populate the given dialog's tabs with instance types, package, and project models.

    This function initializes the core data for various services like 'maya-io', 'nuke', and 'arnold-standalone'. It then fetches the core data, forces a refresh if required, and handles any exceptions by displaying an error message.

    After successfully fetching the data, it processes the instance types, projects, and software packages to create models which are then used to update the UI elements of the provided dialog. The dialog is expected to have tabs that can be hydrated with this core data.

    Args:
        dialog: The dialog object containing tabs that need to be updated with the core data.
        force (bool): If True, forces a refresh of the core data.

    Returns:
        None: The function does not return a value but updates the dialog components in place.

    Raises:
        BaseException: Catches any exception that occurs during the core data initialization and data fetching process, displays an error message, and instructs the user on how to possibly resolve the issue.
    """
    coredata.init("maya-io", "nuke", "arnold-standalone")
    try:
        coredata.data(force=force)
    except BaseException as ex:
        pm.displayError(str(ex))
        pm.displayWarning(
            "Try again after deleting your credentials file (~/.config/conductor/credentials)"
        )
        return

    instance_types_model = coredata.data()["instance_types"].categories
    projects_model = [
        {"name": entry, "description": entry} for entry in coredata.data()["projects"]
    ]
    package_model = _get_package_model(coredata.data()["software"])

    kwargs = {
        "inst_types_model": instance_types_model,
        "package_model": package_model,
        "projects_model": projects_model,
    }
    for tab in dialog.tabs.values():
        tab.hydrate_coredata(**kwargs)


def _get_package_model(package_data):
    """
    Construct a package model from the given package data.

    This function takes package data, iterates over supported host names,
    and for each host, it creates an entry containing the host name, description,
    and a list of supported plugins with their respective versions and descriptions.

    Args:
        package_data (PackageTree): A tree-like object that is provided with ciocore::data.

    Returns:
        list: A list of dictionaries, where each dictionary represents a host and its
              associated plugins. Each host entry contains the keys 'name', 'description',
              and 'plugins', where 'plugins' is a list of plugin entries. Each plugin entry
              is a dictionary with keys 'name' and 'description'.
    """

    result = k.NONE_MODEL
    host_names = package_data.supported_host_names()
    for host_name in host_names:
        host_product, host_version, host_platform = host_name.split(" ")
        entry = {
            "name": host_name,
            "description": f"{host_product} {host_version}",
            "plugins": [],
        }
        plugin_packs = package_data.supported_plugins(host_name)
        for plugin_pack in plugin_packs:
            product = plugin_pack["plugin"]
            versions = plugin_pack["versions"]
            for version in versions:
                plugin_entry_name = f"{host_name}|{product} {version} {host_platform}"
                plugin_entry_description = (
                    f"{product} {version} for {host_product} {host_version}"
                )
                entry["plugins"].append(
                    {"name": plugin_entry_name, "description": plugin_entry_description}
                )
        result.append(entry)
    return result
