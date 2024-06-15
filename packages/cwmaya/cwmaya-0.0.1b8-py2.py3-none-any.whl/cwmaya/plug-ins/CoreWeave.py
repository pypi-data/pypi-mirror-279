import sys
import os

import maya.api.OpenMaya as om
import maya.cmds as cmds

CIODIR = os.environ.get("CWMAYA_CIODIR")
sys.path.append(CIODIR)

from cwmaya.template.helpers.cw_submission_base import cwSubmission
from cwmaya.template.smoke.cw_smoke_submission import cwSmokeSubmission
from cwmaya.template.sim_render.cw_sim_render_submission import cwSimRenderSubmission
from cwmaya.template.chain.cw_chain_submission import cwChainSubmission
from cwmaya.menus import coreweave_menu


def maya_useNewAPI():
    pass


def initializePlugin(obj):

    plugin = om.MFnPlugin(obj, "CoreWeave", "0.0.1-beta.8", "Any")

    try:
        plugin.registerNode(
            "cwSubmission",
            cwSubmission.id,
            cwSubmission.creator,
            cwSubmission.initialize,
            om.MPxNode.kDependNode,
        )

        plugin.registerNode(
            "cwSmokeSubmission",
            cwSmokeSubmission.id,
            cwSmokeSubmission.creator,
            cwSmokeSubmission.initialize,
            om.MPxNode.kDependNode,
        )

        plugin.registerNode(
            "cwSimRenderSubmission",
            cwSimRenderSubmission.id,
            cwSimRenderSubmission.creator,
            cwSimRenderSubmission.initialize,
            om.MPxNode.kDependNode,
        )

        plugin.registerNode(
            "cwChainSubmission",
            cwChainSubmission.id,
            cwChainSubmission.creator,
            cwChainSubmission.initialize,
            om.MPxNode.kDependNode,
        )

        create_storm_shelf()
    except:
        sys.stderr.write("Failed to register submission nodes\n")
        raise

    coreweave_menu.load()


def uninitializePlugin(obj):
    plugin = om.MFnPlugin(obj)

    try:
        remove_storm_shelf()
        plugin.deregisterNode(cwChainSubmission.id)
        plugin.deregisterNode(cwSimRenderSubmission.id)
        plugin.deregisterNode(cwSmokeSubmission.id)
        plugin.deregisterNode(cwSubmission.id)
    except:
        sys.stderr.write("Failed to deregister submission nodes\n")
        raise

    coreweave_menu.unload()


def create_storm_shelf():
    shelf_name = "Storm"

    # Delete the shelf if it already exists
    if cmds.shelfLayout(shelf_name, exists=True):
        cmds.deleteUI(shelf_name, layout=True)

    # Create a new shelf
    cmds.shelfLayout(shelf_name, parent="ShelfLayout")

    # Add buttons to the shelf
    cmds.shelfButton(
        label="My Button",
        command='print("Button Pressed")',
        image1="commandButton.png",  # Path to your icon file
        parent=shelf_name,
    )


def remove_storm_shelf():
    shelf_name = "Storm"
    if cmds.shelfLayout(shelf_name, exists=True):
        cmds.deleteUI(shelf_name, layout=True)
