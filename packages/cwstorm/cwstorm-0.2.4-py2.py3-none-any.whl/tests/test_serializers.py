import unittest

from cwstorm.serializers import default

from cwstorm.dsl.job import Job
from cwstorm.dsl.dag_node import DagNode
from cwstorm.dsl.task import Task
from cwstorm.dsl.cmd import Cmd


class CytoscapeTest(unittest.TestCase):
    def setUp(self):
        DagNode.reset()
        self.job = Job()

    def test_serialize_comment(self):
        self.job.comment("foo")
        serialized = default.serialize(self.job)
        self.assertEqual(serialized["nodes"][0]["data"]["id"], "Job_00000")

    def test_serialize_job_with_children(self):
        self.job.add(Task())
        serialized = default.serialize(self.job)

        self.assertEqual(len(serialized["nodes"]), 2)
        self.assertEqual(len(serialized["edges"]), 1)

    def test_serialize_job_with_references(self):
        render1 = Task().commands(Cmd().argv("render1"))
        render2 = Task().commands(Cmd().argv("render2"))

        self.job.add(render1)
        self.job.add(render2)
        export_1_2 = Task().commands(Cmd().argv("export_1_2"))
        render1.add(export_1_2)
        render2.add(export_1_2)

        serialized = default.serialize(self.job)
        nodes = serialized["nodes"]
        edges = serialized["edges"]

        self.assertEqual(len(nodes), 4)
        self.assertEqual(len(edges), 4)


#        ┌─────┐
#        │ job │
#        └──┬──┘
#           │
#     ┌─────┴───────┐
# ┌───┴───┐     ┌───┴───┐
# │ frame1│     │ frame2│
# └───┬───┘     └───┬───┘
#     └──────┬──────┘
#            │
#        ┌───┴───┐
#        │  ass  │
#        └───┬───┘
