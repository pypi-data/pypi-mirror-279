# -*- coding: utf-8 -*-

import pymel.core as pm

class CwTemplateBase(object):
    
    DEFAULTS = [
        {"attribute": "label", "value": "Job"},
        {
            "attribute": "description",
            "value": "Creates a work task tyo testy the system.",
        },
        {"attribute": "location", "value": "Panama"},
        {"attribute": "author", "value": "jmann"}
    ]

    CONNECTIONS = []

    @classmethod
    def setup(cls, node):
        for attr in cls.DEFAULTS:
            value = attr["value"]
            if type(value) == list:
                for i, v in enumerate(value):
                    node.attr(attr["attribute"])[i].set(v)
            else:
                node.attr(attr["attribute"]).set(value)

        for src, dest in cls.CONNECTIONS:
            src = pm.Attribute(src)
            dest = node.attr(dest)
            if not pm.isConnected(src, dest):
                pm.displayInfo("connectAttr: {} {}".format(src, dest))
                src.connect(dest)

    @classmethod
    def bind(cls, node, dialog):
        dialog.setTitleAndName(node)
        dialog.clear_tabs()

