import unittest
from cwstorm.dsl.cmd import Cmd
from cwstorm.dsl.dag_node import DagNode


class InitializeTest(unittest.TestCase):

    def setUp(self):
        DagNode.reset()
        self.node = Cmd()

    def test_argv_attribute(self):
        self.node.argv("foo")
        self.assertEqual(self.node.argv(), ["foo"])

    def test_bad_attribute(self):
        with self.assertRaises(AttributeError):
            self.node.foo("foo")
