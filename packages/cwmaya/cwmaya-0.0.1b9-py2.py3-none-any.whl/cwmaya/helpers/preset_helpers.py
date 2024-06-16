
# -*- coding: utf-8 -*-

import pymel.core as pm

def save_preset(node, preset=None):
    """
    Save the current state of the node as a preset.
    """
    if not preset:
        preset = prompt_for_preset_name()
    if not preset:
        return

    pm.nodePreset( save=(node, preset) )

    print(f"Saved preset: {preset} for node: {node}")

def load_preset(node, preset, dialog=None):
    """
    Load the specified preset onto the node.
    """
    print(f"Loading preset: {preset} onto node: {node}")
    pm.nodePreset( load=(node, preset) )
    if dialog:
        dialog.load_template(node)

def prompt_for_preset_name():
    """
    Prompt the user for a preset name.
    """
    result = pm.promptDialog(
        title='Save Preset',
        message='Enter Name:',
        button=['OK', 'Cancel'],
        defaultButton='OK',
        cancelButton='Cancel',
        dismissString='Cancel')

    if not (result == 'OK'):
        return None
    
    preset = pm.promptDialog(query=True, text=True)
    if not pm.nodePreset(isValidName=preset):
        pm.error("Invalid preset name")
        return None
    return preset
