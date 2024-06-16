"""
This metaclass, NodeMeta, is designed to dynamically create accessor methods for class attributes based on a predefined schema.

The schema is provided through a class-level dictionary named `ATTRS`, where each key-value pair represents an attribute and its options. The metaclass takes this schema and generates getter/setter methods that include validation and type enforcement as defined in the `ATTRS` dictionary.

The generated accessors allow for setting new values to attributes with appropriate validation and getting their current values. Additionally, for list-type attributes, methods are created to append new items to the list while applying the same validation rules.

By utilizing this metaclass, classes can ensure that their attributes adhere strictly to the specified types and constraints, providing a robust way of managing data integrity within instances of those classes.

Usage:
    To use NodeMeta, define a class with NodeMeta as its metaclass and provide an `ATTRS` dictionary with the desired attribute specifications. The metaclass will automatically generate the necessary accessor methods during class creation.

Example:
    class ExampleNode(metaclass=NodeMeta):
        ATTRS = {
            'name': {'type': 'str', 'default': 'Unnamed', 'validator': some_validation_function},
            'value': {'type': 'int:list', 'default': 1, 'validator': another_validation_function}
        }
        
        # Custom validation methods can be defined as needed.
        def some_validation_function(self, value):
            # Implement validation logic here
            pass
        
        def another_validation_function(self, value):
            # Implement validation logic here
            pass

After defining the class, instances of it will have `name` and `value` as accessible properties with custom getter/setter and validation logic applied.
"""

from copy import deepcopy


class NodeMeta(type):
    def __new__(cls, name, bases, attrs):
        """Build accessors for each attribute in ATTRS.

        ATTRS is a dict of attribute names to dicts of attribute options that help to validate access to the attribute.
        """
        if attrs.get("ATTRS"):
            attr_map = deepcopy(attrs["ATTRS"])
            for key in attr_map:
                kwargs = attr_map[key]
                datatype = kwargs.pop("type")
                result = cls.build_accessors(key, datatype, **kwargs)
                for entry in result:
                    attrs[entry["name"]] = entry["function"]

        return super().__new__(cls, name, bases, attrs)

    @classmethod
    def build_accessors(cls, name, datatype, **kwargs):
        datatype = datatype.split(":")
        is_list = False
        if len(datatype) > 1:
            datatype = datatype[1]
            is_list = True
        else:
            datatype = datatype[0]
        if datatype == "str":
            if is_list:
                return cls.build_list_string_accessors(name, **kwargs)
            return cls.build_string_accessors(name, **kwargs)
        elif datatype == "int":
            if is_list:
                return cls.build_list_int_accessors(name, **kwargs)
            return cls.build_int_accessors(name, **kwargs)
        elif datatype == "bool":
            if is_list:
                return cls.build_list_bool_accessors(name, **kwargs)
            return cls.build_bool_accessors(name, **kwargs)
        elif datatype == "Cmd":
            if is_list:
                return cls.build_list_cmd_accessors(name, **kwargs)
            return cls.build_cmd_accessors(name, **kwargs)
        elif datatype == "dict":
            if is_list:
                return cls.build_list_dict_accessors(name, **kwargs)
            return cls.build_dict_accessors(name, **kwargs)
        # we got here because we don't know how to handle the datatype
        raise TypeError("Invalid type: %s" % datatype)

    @classmethod
    def build_string_accessors(cls, name, **kwargs):
        default = kwargs.get("default")
        prop = "_{}".format(name)
        
        accessor_name = name

        def accessor(self, *args):
            if len(args) > 1:
                raise TypeError("Accessor takes at most one argument")
            if len(args) == 1:
                self.validate_string(accessor_name, args[0], **kwargs)
                setattr(self, prop, args[0])
                return self
            if hasattr(self, prop):
                return getattr(self, prop)
            return default

        return [{"name": accessor_name, "function": accessor}]

    @classmethod
    def build_int_accessors(cls, name, **kwargs):
        default = kwargs.get("default")
        prop = "_{}".format(name)
        accessor_name = name

        def accessor(self, *args):
            if len(args) > 1:
                raise TypeError("Accessor takes at most one argument")
            if len(args) == 1:
                self.validate_int(accessor_name, args[0], **kwargs)
                setattr(self, prop, args[0])
                return self
            if hasattr(self, prop):
                return getattr(self, prop)
            return default

        return [{"name": accessor_name, "function": accessor}]

    @classmethod
    def build_bool_accessors(cls, name, **kwargs):
        default = kwargs.get("default", False)
        prop = "_{}".format(name)
        accessor_name = name

        def accessor(self, *args):
            if len(args) > 1:
                raise TypeError("Accessor takes at most one argument")
            if len(args) == 1:
                self.validate_bool(accessor_name, args[0], **kwargs)
                setattr(self, prop, args[0])
                return self
            if hasattr(self, prop):
                return getattr(self, prop)
            return default

        return [{"name": accessor_name, "function": accessor}]


 

    @classmethod
    def build_list_string_accessors(cls, name, **kwargs):
        default = kwargs.get("default", [])
        prop = "_{}".format(name)
        accessor_name = name
        appender_name = "push_{}".format(name)

        def accessor(self, *args):
            if len(args) > 0:
                self.validate_string(accessor_name, *args, **kwargs)
                setattr(self, prop, list(args))
                return self
            if hasattr(self, prop):
                return getattr(self, prop)
            return default

        def appender(self, *args):
            self.validate_string(appender_name, *args, **kwargs)
            if hasattr(self, prop):
                value = getattr(self, prop)
            else:
                value = []
            value.extend(args)
            setattr(self, prop, list(value))
            return self

        return [
            {"name": accessor_name, "function": accessor},
            {"name": appender_name, "function": appender},
        ]

    @classmethod
    def build_list_int_accessors(cls, name, **kwargs):
        default = kwargs.get("default", [])
        prop = "_{}".format(name)
        accessor_name = name
        appender_name = "push_{}".format(name)

        def accessor(self, *args):
            if len(args) > 0:
                self.validate_int(accessor_name, *args, **kwargs)
                setattr(self, prop, list(args))
                return self
            if hasattr(self, prop):
                return getattr(self, prop)
            return default

        def appender(self, *args):
            self.validate_int(appender_name, *args, **kwargs)
            if hasattr(self, prop):
                value = getattr(self, prop)
            else:
                value = []
            value.extend(args)
            setattr(self, prop, list(value))
            return self

        return [
            {"name": accessor_name, "function": accessor},
            {"name": appender_name, "function": appender},
        ]
        
    @classmethod
    def build_list_bool_accessors(cls, name, **kwargs):
        default = kwargs.get("default", [])
        prop = "_{}".format(name)
        accessor_name = name
        appender_name = "push_{}".format(name)

        def accessor(self, *args):
            if len(args) > 0:
                self.validate_bool(accessor_name, *args, **kwargs)
                setattr(self, prop, list(args))
                return self
            if hasattr(self, prop):
                return getattr(self, prop)
            return default

        def appender(self, *args):
            self.validate_bool(appender_name, *args, **kwargs)
            if hasattr(self, prop):
                value = getattr(self, prop)
            else:
                value = []
            value.extend(args)
            setattr(self, prop, list(value))
            return self

        return [
            {"name": accessor_name, "function": accessor},
            {"name": appender_name, "function": appender},
        ]

    @classmethod
    def build_cmd_accessors(cls, name, **kwargs):
        prop = "_{}".format(name)
        accessor_name = name

        def accessor(self, *args):
            if len(args) > 1:
                raise TypeError("Accessor takes at most one argument")
            if len(args) == 1:
                self.validate_cmd(accessor_name, args[0], **kwargs)
                setattr(self, prop, args[0])
                return self
            if hasattr(self, prop):
                return getattr(self, prop)
            return None

        return [{"name": accessor_name, "function": accessor}]

    @classmethod
    def build_list_cmd_accessors(cls, name, **kwargs):
        prop = "_{}".format(name)
        accessor_name = name
        appender_name = "push_{}".format(name)

        def accessor(self, *args):
            if len(args) > 0:
                self.validate_cmd(accessor_name, *args, **kwargs)
                setattr(self, prop, list(args))
                return self
            if hasattr(self, prop):
                return getattr(self, prop)
            return []

        def appender(self, *args):
            self.validate_cmd(appender_name, *args, **kwargs)
            if hasattr(self, prop):
                value = getattr(self, prop)
            else:
                value = []
            value.extend(args)
            setattr(self, prop, list(value))
            return self

        return [
            {"name": accessor_name, "function": accessor},
            {"name": appender_name, "function": appender},
        ]

    @classmethod
    def build_dict_accessors(cls, name, **kwargs):
        default = kwargs.get("default", {})
        prop = "_{}".format(name)
        accessor_name = name
        updater_name = "update_{}".format(name)

        def accessor(self, rhs=None):
            if rhs:
                rhs = deepcopy(rhs)
                self.validate_dict(accessor_name, rhs, **kwargs)
                setattr(self, prop, rhs)
                return self
            if hasattr(self, prop):
                return getattr(self, prop)
            return default

        def updater(self, rhs):
            rhs = deepcopy(rhs)
            self.validate_dict(updater_name, rhs, **kwargs)
            if hasattr(self, prop):
                value = getattr(self, prop)
            else:
                value = {}
            value = {**value, **rhs}
            setattr(self, prop, value)
            return self

        return [
            {"name": accessor_name, "function": accessor},
            {"name": updater_name, "function": updater},
        ]

    @classmethod
    def build_list_dict_accessors(cls, name, **kwargs):
        default = kwargs.get("default", [])
        prop = "_{}".format(name)
        accessor_name = name
        appender_name = "push_{}".format(name)

        def accessor(self, *args):
            if len(args) > 0:
                self.validate_dict(accessor_name, *args, **kwargs)
                setattr(self, prop, list(args))
                return self
            if hasattr(self, prop):
                return getattr(self, prop)
            return default

        def appender(self, *args):
            self.validate_dict(appender_name, *args, **kwargs)
            if hasattr(self, prop):
                value = getattr(self, prop)
            else:
                value = []
            value.extend(args)
            setattr(self, prop, list(value))
            return self

        return [
            {"name": accessor_name, "function": accessor},
            {"name": appender_name, "function": appender},
        ]
