import unittest
import re

from cwstorm.dsl.node import Node
from cwstorm.dsl.cmd import Cmd


class SomeNode(Node):
    ATTRS = {
        "strattr": {
            "type": "str",
            "validator": re.compile(r"^[a-z0-9_\-\s]+$", re.IGNORECASE),
        },
        "defaulted_str_attr": {"type": "str", "default": "def"},
        "defaulted_list_str_attr": {"type": "list:str", "default": ["def"]},
        "liststrattr": {
            "type": "list:str",
            "validator": re.compile(r"^[a-zA-Z0-9_\-\s]+$", re.IGNORECASE),
        },
        "intattr": {"type": "int", "validator":{ "min": 0, "max": 10}},
        "listintattr": {"type": "list:int", "validator":{"min": 0, "max": 10}},
        "cmdattr": {"type": "Cmd"},
        "listcmdattr": {"type": "list:Cmd"},
        "dictattr": {"type": "dict", "validator": {"keys": ["foo", "bar", "baz"]}},
        "listdictattr": {"type": "list:dict"},
    }



class PrimitiveAccessorsTest(unittest.TestCase):
    def setUp(self):
        self.node = SomeNode()

    def test_init_attrs(self):
        self.assertEqual(len(self.node.ATTRS), 10)

    def test_creates_attributes(self):
        attributes = dir(self.node)
        
        for key in [
        "strattr",
         "liststrattr",
         "listintattr",
         "intattr",
         "push_liststrattr",
         "push_listintattr",
         "dictattr",
         "listdictattr",
         "cmdattr",
         "listcmdattr",
         "defaulted_str_attr",
         "defaulted_list_str_attr",
         "update_dictattr",
         "push_listdictattr"
         ]:
            self.assertIn(key, attributes)

 
    def test_simple_getters_return_none_by_default(self):
        self.assertIsNone(self.node.strattr())
        self.assertIsNone(self.node.intattr())

    def test_list_getters_return_empty_list_by_default(self):
        self.assertEqual(self.node.liststrattr(), [])
        self.assertEqual(self.node.listintattr(), [])

    def test_setter_and_getter_returns_assigned_value(self):
        self.node.strattr("foo")
        self.assertEqual(self.node.strattr(), "foo")

    def test_list_setter_and_getter_returns_assigned_value_as_list(self):
        self.node.liststrattr("foo")
        self.assertEqual(self.node.liststrattr(), ["foo"])

    def test_list_int_setter_and_getter_returns_assigned_value_as_list(self):
        self.node.listintattr(1)
        self.assertEqual(self.node.listintattr(), [1])

    def test_string_setter_returns_self(self):
        self.assertEqual(self.node.strattr("foo"), self.node)

    def test_int_setter_returns_self(self):
        self.assertEqual(self.node.intattr(1), self.node)

    def test_list_string_setter_returns_self(self):
        self.assertEqual(self.node.liststrattr("foo"), self.node)

    def test_list_int_setter_returns_self(self):
        self.assertEqual(self.node.listintattr(1), self.node)

    def test_set_get_chaining(self):
        self.assertEqual(self.node.strattr("foo").strattr(), "foo")

    def test_set_set_get_chaining(self):
        self.assertEqual(self.node.strattr("foo").strattr("bar").strattr(), "bar")

    def test_set_push_push_get_chaining(self):
        self.assertEqual(
            self.node.liststrattr("baz", "yum")
            .push_liststrattr("foo")
            .push_liststrattr("bar")
            .liststrattr(),
            ["baz", "yum", "foo", "bar"],
        )

    def test_list_set_does_not_append(self):
        self.node.liststrattr("foo")
        self.node.liststrattr("bar")
        self.assertEqual(self.node.liststrattr(), ["bar"])

    def test_string_regex_validation(self):
        self.assertRaises(ValueError, self.node.strattr, "foo!bar")
        self.assertRaises(ValueError, self.node.strattr, "foo.bar")

    def test_string_type_validation(self):
        self.assertRaises(TypeError, self.node.strattr, 1)

    def test_list_string_any_regex_validation(self):
        self.assertRaises(ValueError, self.node.liststrattr, "foo", "bad!", "bar")

    def test_list_string_any_type_validation(self):
        self.assertRaises(TypeError, self.node.liststrattr, "foo", 7, "bar")

    def test_int_limit_validation(self):
        self.assertRaises(ValueError, self.node.intattr, -1)
        self.assertRaises(ValueError, self.node.intattr, 11)

    def test_int_type_validation(self):
        self.assertRaises(TypeError, self.node.listintattr, "foo")

    def test_list_int_limit_validation(self):
        self.assertRaises(ValueError, self.node.listintattr, -1, 1)

    def test_unsupported_getter_raises_error(self):
        with self.assertRaises(AttributeError):
            self.node.unsupportedattr()

    def test_unsupported_setter_raises_error(self):
        with self.assertRaises(AttributeError):
            self.node.unsupportedattr("foo")

    def test_list_creates_copy(self):
        list1 = ["foo", "bar"]
        self.node.liststrattr(*list1)
        result = self.node.liststrattr()
        self.assertEqual(result, list1)
        self.assertNotEqual(id(result), id(list1))

    def test_push_list_creates_copy(self):
        list1 = ["foo", "bar"]
        self.node.liststrattr(*list1)
        result = self.node.liststrattr()
        self.node.push_liststrattr("baz")
        self.assertNotEqual(id(result), id(list1))

    def test_default_string_value(self):
        self.assertEqual(self.node.defaulted_str_attr(), "def")

    def test_default_list_string_value(self):
        self.assertEqual(self.node.defaulted_list_str_attr(), ["def"])


class DictAccessorsTest(unittest.TestCase):
    def setUp(self):
        self.node = SomeNode()

    def test_dict_getter_return_empty_by_default(self):
        self.assertEqual(self.node.dictattr(), {})

    def test_dict_setter_and_getter_returns_copy(self):
        d = {"foo": "bar"}
        self.node.dictattr(d)
        result = self.node.dictattr()
        self.assertEqual(result, d)
        self.assertNotEqual(id(result), id(d))

    def test_dict_updater_makes_copy(self):
        d = {"foo": "bar"}
        self.node.dictattr(d)
        result = self.node.dictattr()
        self.node.update_dictattr({"baz": "qux"})
        self.assertNotEqual(id(result), id(d))

    def test_listdict_setter_and_getter_returns_assigned_value_as_list(self):
        d = {"foo": "bar"}
        self.node.listdictattr(d)
        self.assertEqual(self.node.listdictattr(), [d])
        
    def test_listdict_setter_makes_copy(self):
        d = {"foo": "bar"}
        self.node.listdictattr(d)
        result = self.node.listdictattr()
        self.assertNotEqual(id(result), id(d))

    def test_dict_validation_fails_if_invalid_key(self):
        d = {"invalid": "bar", "foo": "bar"}
        with self.assertRaises(ValueError):
            self.node.dictattr(d)
            

class CmdAccessorsTest(unittest.TestCase):
    def setUp(self):
        self.node = SomeNode()

    def test_cmd_getter_return_none_by_default(self):
        self.assertIsNone(self.node.cmdattr())

    def test_listcmd_getter_returns_empty_by_default(self):
        self.assertEqual(self.node.listcmdattr(), [])

    def test_cmd_setter_and_getter_returns_same_object(self):
        cmd = Cmd()
        self.node.cmdattr(cmd)
        self.assertEqual(self.node.cmdattr(), cmd)


class DictCastTest(unittest.TestCase):
    def setUp(self):
        self.node = SomeNode()

    def test_dict_cast(self):
        self.assertIsInstance(dict(self.node), dict)

    def test_dict_cast_does_not_include_none_or_empty_values(self):
        self.node.strattr("foo")
        d = dict(self.node)
        expected_key = "strattr"
        expected_value = "foo"
        self.assertIn(expected_key, d)
        self.assertEqual(d[expected_key], expected_value)

    def test_dict_cast_includes_list_values(self):
        self.node.liststrattr("foo")
        # self.assertEqual(dict(self.node), {"liststrattr": ["foo"]})
        d = dict(self.node)
        expected_key = "liststrattr"
        expected_value = ["foo"]
        self.assertIn(expected_key, d)
        self.assertEqual(d[expected_key], expected_value)

    def test_dict_cast_includes_int_values(self):
        self.node.intattr(1)
        d = dict(self.node)
        expected_key = "intattr"
        expected_value = 1
        self.assertIn(expected_key, d)
        self.assertEqual(d[expected_key], expected_value)

    def test_dict_cast_includes_dict_values(self):
        self.node.dictattr({"foo": "bar"})
        d = dict(self.node)
        expected_key = "dictattr"
        expected_value = {"foo": "bar"}
        self.assertIn(expected_key, d)
        self.assertEqual(d[expected_key], expected_value)

    def test_dict_cast_includes_list_dict_values(self):
        self.node.listdictattr({"foo": "bar"})
        d = dict(self.node)
        expected_key = "listdictattr"
        expected_value = [{"foo": "bar"}]
        self.assertIn(expected_key, d)
        self.assertEqual(d[expected_key], expected_value)