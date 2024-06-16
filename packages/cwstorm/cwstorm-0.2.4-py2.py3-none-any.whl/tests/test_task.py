import unittest
from cwstorm.dsl.task import Task
from cwstorm.dsl.dag_node import DagNode


class TaskTest(unittest.TestCase):

    
    def setUp(self):
        DagNode.reset()
        self.root = DagNode()
        self.a = Task()
        self.b = Task()
        self.root.add(self.a, self.b)
        
        self.c = Task()

        self.a.add(self.c)
        self.b.add(self.c)


    def test_is_instance(self):
        self.assertFalse(self.c.is_reference(self.a))
        self.assertTrue(self.c.is_reference(self.b))
    
    def test_is_original(self):
        self.assertTrue(self.c.is_original(self.a))
        self.assertFalse(self.c.is_original(self.b))
