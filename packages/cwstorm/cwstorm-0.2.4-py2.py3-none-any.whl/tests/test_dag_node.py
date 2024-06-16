import unittest

from cwstorm.dsl.dag_node import DagNode, VALID_NAME_REGEX
from cwstorm.dsl.task import Task


class Foo(DagNode):
    pass


class InitTest(unittest.TestCase):
    def setUp(self):
        DagNode.reset()
        self.node = DagNode()


    def test_subclass_registers_node(self):
        Foo()
        self.assertEqual(len(DagNode.instances.keys()), 2)

    def test_init_creates_name(self):
        self.assertEqual(self.node.name(), "DagNode_00000")

    def test_init_creates_with_name_arg(self):
        node = DagNode("Hello")
        self.assertEqual(node.name(), "Hello")

    def test_init_creates_unique_default_names(self):
        other = DagNode()
        self.assertEqual(self.node.name(), "DagNode_00000")
        self.assertEqual(other.name(), "DagNode_00001")

    def test_init_creates_unique_names_for_bug_described(self):
        """
        Bug when Sim_1-7 is created twice. It is not renamed.
        """
        node1 = DagNode("Sim_1-7")
        node2 = DagNode("Sim_1-7")
        self.assertNotEqual(node1.name(), node2.name())

    def test_subclass_init_creates_unique_default_names(self):
        other0 = Foo()
        other1 = Foo()
        self.assertNotEqual(other0.name(), other1.name())


class AddMethodTest(unittest.TestCase):
    def setUp(self):
        DagNode.reset()
        self.rootNode = DagNode()
        self.a = Task()
        self.b = Task()
        self.rootNode.add(self.a, self.b)

    def test_add_children(self):
        self.rootNode.add(Task(), Task())
        self.assertEqual(len(self.rootNode.children), 4)
        self.assertEqual(len(self.rootNode.children[2].parents), 1)

    def test_add_anything_other_than_tasks_raises(self):
        self.assertRaises(TypeError, self.rootNode.add, "foo")

    def test_dont_add_existing_children(self):
        self.rootNode.add(self.b)
        self.assertEqual(len(self.rootNode.children), 2)

    def test_add_returns_self(self):
        self.assertEqual(self.rootNode.add(Task()), self.rootNode)


class TitleTest(unittest.TestCase):
    def setUp(self):
        DagNode.reset()
        self.node = DagNode()

    def test_init_name_valid_against_regex(self):
        value = self.node.name()
        self.assertRegex(value, VALID_NAME_REGEX)

    def test_init_name_unique(self):
        other = DagNode()
        self.assertNotEqual(self.node.name(), other.name())

    def test_name_setter_raises(self):
        with self.assertRaises(TypeError):
            self.node.name("foo")

    def test_cast_to_string_is_name(self):
        self.assertEqual(str(self.node), self.node.name())

    def test_several_name_unique_names(self):
        other1 = DagNode()
        task1 = Task()

        self.assertEqual(self.node.name(), "DagNode_00000")
        self.assertEqual(other1.name(), "DagNode_00001")
        self.assertEqual(task1.name(), "Task_00000")


class RelationshipTest(unittest.TestCase):
    def setUp(self):
        DagNode.reset()
        self.rootNode = DagNode()
        self.a = Task()
        self.b = Task()
        self.rootNode.add(self.a, self.b)

    def test_is_leaf(self):
        self.assertTrue(self.a.is_leaf())

    def test_is_not_leaf(self):
        self.assertFalse(self.rootNode.is_leaf())

    def test_is_root(self):
        self.assertTrue(self.rootNode.is_root())

    def test_is_not_root(self):
        self.assertFalse(self.a.is_root())

    def test_parent_list(self):
        self.assertEqual(len(self.a.parents), 1)
        self.assertEqual(self.a.parents[0], self.rootNode)

    def test_multi_parent_list(self):
        c = Task()
        self.a.add(c)
        self.b.add(c)
        self.assertEqual(len(c.parents), 2)

    def test_dont_add_to_existing_parents(self):
        self.rootNode.add(self.a)
        self.assertEqual(len(self.a.parents), 1)

    def test_count_ancestors(self):
        grandparent1 = Task()
        grandparent2 = Task()
        grandparent3 = Task()
        parent1 = Task()
        parent2 = Task()

        me = Task()

        grandparent1.add(parent1, parent2)
        grandparent2.add(parent1, parent2)
        grandparent3.add(parent1)
        parent1.add(me)
        parent2.add(me)

        ancestors = me.count_ancestors()

        self.assertEqual(ancestors, 5)

    def test_count_descendents(self):
        child1 = Task()
        child2 = Task()
        child3 = Task()
        child4 = Task()
        grandchild1 = Task()
        grandchild2 = Task()
        grandchild3 = Task()
        greatgrandchild1 = Task()
        greatgrandchild2 = Task()

        me = Task()

        me.add(child1, child2, child3, child4)
        child1.add(grandchild1, grandchild2)
        child2.add(grandchild2, grandchild3)
        grandchild1.add(greatgrandchild2)
        grandchild3.add(greatgrandchild1, greatgrandchild2)

        descendants = me.count_descendents()

        self.assertEqual(descendants, 9)
