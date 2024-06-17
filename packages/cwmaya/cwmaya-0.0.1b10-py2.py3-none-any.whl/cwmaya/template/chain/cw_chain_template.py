# -*- coding: utf-8 -*-

import pymel.core as pm

from cwmaya.tabs import general_tab, simple_tab, job_tab
from cwmaya.template.helpers import cw_template_base


class CwChainTemplate(cw_template_base.CwTemplateBase):

    DEFAULTS = [
        {"attribute": "label", "value": "Job_{sequence}"},
        {
            "attribute": "description",
            "value": "Creates a fluid sim, renders it with Arnold through Maya, and finally makes a movie.",
        },
        {"attribute": "location", "value": "Panama"},
        {"attribute": "author", "value": "jmann"},
        {"attribute": "wrkLabel", "value": "Sim_{sequence}"},
        {"attribute": "wrkPreemptible", "value": True},
        {
            "attribute": "wrkCommands",
            "value": ["maya - batch -export-a-simulation {seqstart} {seqend}"],
        },
        {"attribute": "wrkOutputPath", "value": "/myproject/caches"},
        {"attribute": "chunkSize", "value": 1},
        {"attribute": "useCustomRange", "value": True},
        {"attribute": "customRange", "value": "1-7"},
        {"attribute": "useScoutFrames", "value": True},
        {"attribute": "scoutFrames", "value": "fml:5"},
    ]

    CONNECTIONS = [
        ("defaultRenderGlobals.startFrame", "startFrame"),
        ("defaultRenderGlobals.endFrame", "endFrame"),
        ("defaultRenderGlobals.byFrameStep", "byFrame"),
        ("time1.outTime", "currentTime"),
    ]

    @classmethod
    def bind(cls, node, dialog):

        super().bind(node, dialog)

        pm.setParent(dialog.tabLayout)
        dialog.tabs["general_tab"] = general_tab.GeneralTab()

        pm.setParent(dialog.tabLayout)
        dialog.tabs["wrk_tab"] = simple_tab.SimpleTab()

        pm.setParent(dialog.tabLayout)
        dialog.tabs["job_tab"] = job_tab.JobTab()

        pm.setParent(dialog.tabLayout)

        dialog.tabLayout.setTabLabel((dialog.tabs["general_tab"], "Frames"))
        dialog.tabLayout.setTabLabel((dialog.tabs["wrk_tab"], "Work"))
        dialog.tabLayout.setTabLabel((dialog.tabs["job_tab"], "Job"))

        dialog.tabs["general_tab"].bind(node)
        dialog.tabs["wrk_tab"].bind(node, "wrk")
        dialog.tabs["job_tab"].bind(node)
        dialog.tabLayout.setSelectTabIndex(2)
