# from __future__ import unicode_literals
import os
import json

from cwmaya.template.helpers.cw_submission_base import cwSubmission
from cwmaya.template.helpers import (
    task_attributes,
    frames_attributes,
    job_attributes,
    context,
)


# pylint: disable=import-error
import maya.api.OpenMaya as om

MAX_FILES_PER_UPLOAD = 4


def maya_useNewAPI():
    pass


class cwChainSubmission(cwSubmission):

    # Declare
    aWorkTask = None
    aFramesAttributes = None

    id = om.MTypeId(0x880505)

    def __init__(self):
        """Initialize the class."""
        super(cwChainSubmission, self).__init__()

    @staticmethod
    def creator():
        return cwChainSubmission()

    @classmethod
    def isAbstractClass(cls):
        return False

    @classmethod
    def initialize(cls):
        """Create the static attributes."""
        om.MPxNode.inheritAttributesFrom("cwSubmission")
        cls.aWorkTask = task_attributes.initialize("wrk", "wk", cls.aOutput)
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
        work_values = task_attributes.getValues(data, self.aWorkTask)

        main_sequence = sequences["main_sequence"]
        scout_sequence = sequences["scout_sequence"] or []

        job = job_attributes.computeJob(job_values, context=static_context)

        next_target = job

        scenefile = static_context["scenepath"]
        scene_upload_tasks = task_attributes.generateUploadTasks([scenefile], "Scene")

        # get chunks in reverse order to build the chain

        chunks = main_sequence.chunks()
        chunks.reverse()
        for chunk in chunks:
            dynamic_context = context.getDynamic(static_context, chunk)
            work_task = task_attributes.computeTask(
                work_values, context=dynamic_context
            )
            if scout_sequence:
                if chunk.intersects(scout_sequence):
                    work_task.initial_state("START")
                else:
                    work_task.initial_state("HOLD")

            # work_task.add(*scene_upload_tasks)

            next_target.add(work_task)
            next_target = work_task

        return job
