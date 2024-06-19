"""
Module to manage the context in which strings are interpolated.

Static context is the context that is the same for all frames in a sequence.
Dynamic context is the context that changes with each chunk.
"""

import os
import maya.cmds as cmds
import socket


def getStatic(this_node, sequences=None):

    scenepath = cmds.file(q=True, sn=True)
    scenename = os.path.splitext(cmds.file(q=True, sn=True, shn=True))[0]
    scenedir = os.path.dirname(scenepath)
    mayaprojdir = cmds.workspace(q=True, rd=True).rstrip("/")
    imagesdir = cmds.workspace(expandName=cmds.workspace(fileRuleEntry="images"))

    nodename = this_node.name()
    hostname = socket.getfqdn()
    username = os.getlogin()

    result = {
        "nodename": nodename,
        "scenepath": scenepath,
        "scenename": scenename,
        "scenedir": scenedir,
        "mayaprojdir": mayaprojdir,
        "imagesdir": imagesdir,
        "hostname": hostname,
        "username": username,
    }

    if sequences and sequences["main_sequence"]:
        result["sequence"] = str(sequences["main_sequence"])
        result["seqstart"] = str(sequences["main_sequence"].start)
        result["seqend"] = str(sequences["main_sequence"].end)
        result["seqlen"] = str(len(sequences["main_sequence"]))

    return result


def getDynamic(static_context, chunk):
    context = static_context.copy()
    context["chunk"] = str(chunk)
    context["start"] = str(chunk.start)
    context["end"] = str(chunk.end)
    context["step"] = str(chunk.step)
    context["chunklen"] = str(len(chunk))
    return context
