# from __future__ import unicode_literals
import json

from cwmaya.template.helpers.cw_submission_base import cwSubmission
from cwmaya.template.helpers import task_attributes, job_attributes, context

# pylint: disable=import-error
import maya.api.OpenMaya as om

MAX_FILES_PER_UPLOAD = 4


def maya_useNewAPI():
    pass


class cwSmokeSubmission(cwSubmission):

    aWorkTask = None

    id = om.MTypeId(0x880503)

    def __init__(self):
        """Initialize the class."""
        super(cwSmokeSubmission, self).__init__()

    @staticmethod
    def creator():
        return cwSmokeSubmission()

    @classmethod
    def isAbstractClass(cls):
        return False

    @classmethod
    def initialize(cls):
        """Create the static attributes."""
        om.MPxNode.inheritAttributesFrom("cwSubmission")
        cls.aWorkTask = task_attributes.initialize("wrk", "wk", cls.aOutput)

    def computeTokens(self, data):
        """Compute output json from input attributes."""
        this_node = om.MFnDependencyNode(self.thisMObject())
        static_context = context.getStatic(this_node)
        result = json.dumps(static_context)
        return result

    def computeJob(self, data):

        this_node = om.MFnDependencyNode(self.thisMObject())
        static_context = context.getStatic(this_node)

        job_values = job_attributes.getValues(data, self.aJob)
        work_values = task_attributes.getValues(data, self.aWorkTask)

        job = job_attributes.computeJob(job_values, context=static_context)
        work_task = task_attributes.computeTask(work_values, context=static_context)

        job.add(work_task)

        scenefile = static_context["scenepath"]
        scene_upload_tasks = task_attributes.generateUploadTasks([scenefile], "Scene")
        work_task.add(*scene_upload_tasks)

        return job
