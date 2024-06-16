# from __future__ import unicode_literals
import os
import json

from cwmaya.template.helpers.cw_submission_base import cwSubmission
from cwmaya.template.helpers import task_attributes, frames_attributes, job_attributes, context


# pylint: disable=import-error
import maya.api.OpenMaya as om

MAX_FILES_PER_UPLOAD = 4


def maya_useNewAPI():
    pass


class cwSimRenderSubmission(cwSubmission):

    # Declare
    aSimTask = None
    aRenderTask = None
    aQuicktimeTask = None
    aFramesAttributes = None

    id = om.MTypeId(0x880504)

    def __init__(self):
        """Initialize the class."""
        super(cwSimRenderSubmission, self).__init__()

    @staticmethod
    def creator():
        return cwSimRenderSubmission()

    @classmethod
    def isAbstractClass(cls):
        return False

    @classmethod
    def initialize(cls):
        """Create the static attributes."""
        om.MPxNode.inheritAttributesFrom("cwSubmission")
        cls.aSimTask = task_attributes.initialize("sim", "sm", cls.aOutput)
        cls.aRenderTask = task_attributes.initialize("rnd", "rd", cls.aOutput)
        cls.aQuicktimeTask = task_attributes.initialize("qtm", "qt", cls.aOutput)
        cls.aFramesAttributes = frames_attributes.initialize(cls.aOutput, cls.aTokens)

    def computeTokens(self, data):
        """Compute output json from input attributes."""
        sequences = frames_attributes.getSequences(data, self.aFramesAttributes)
        this_node = om.MFnDependencyNode(self.thisMObject())
        static_context = context.getStatic(this_node, sequences)
        chunk = sequences["main_sequence"].chunks()[0]
        dynamic_context = context.getDynamic(static_context, chunk)
        result = json.dumps(dynamic_context)
        return result

    def computeJob(self, data):
        """Compute output json from input attributes."""

        sequences = frames_attributes.getSequences(data, self.aFramesAttributes)
        this_node = om.MFnDependencyNode(self.thisMObject())
        static_context = context.getStatic(this_node, sequences)

        job_values = job_attributes.getValues(data, self.aJob)
        sim_values = task_attributes.getValues(data, self.aSimTask)
        render_values = task_attributes.getValues(data, self.aRenderTask)
        quicktime_values = task_attributes.getValues(data, self.aQuicktimeTask)

        main_sequence = sequences["main_sequence"]
        scout_sequence = sequences["scout_sequence"] or []

        job = job_attributes.computeJob(job_values, context=static_context)
        sim_task = task_attributes.computeTask(sim_values, context=static_context)
        quicktime_task = task_attributes.computeTask(
            quicktime_values, context=static_context
        )

        job.add(quicktime_task)

        for chunk in main_sequence.chunks():
            dynamic_context = context.getDynamic(static_context, chunk)
            render_task = task_attributes.computeTask(
                render_values, context=dynamic_context
            )
            if scout_sequence:
                if chunk.intersects(scout_sequence):
                    render_task.initial_state("START")
                else:
                    render_task.initial_state("HOLD")
            quicktime_task.add(render_task)
            render_task.add(sim_task)

        scenefile = static_context["scenepath"]
        scene_upload_tasks = task_attributes.generateUploadTasks([scenefile], "Scene")
        sim_task.add(*scene_upload_tasks)

        return job
