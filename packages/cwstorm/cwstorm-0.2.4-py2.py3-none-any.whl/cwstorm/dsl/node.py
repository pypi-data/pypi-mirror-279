from cwstorm.dsl.node_metaclass import NodeMeta


class Node(object, metaclass=NodeMeta):

    """Parent class for serializeable nodes.

             Node
              |
          __________
         |          |
        Cmd      DagNode
                    |
                ____________________
               |          |         |
              Task        Job     Upload

    Subclassesshould specify the attributes to be serialized in a class attribute called
    ATTRS. This is a dict keyed by attribute name, with values specifying the
    attribute type and any additional validation constraints.

    The type is specified as a
    string, with the following options:
    "str" - string
    "int" - integer
    "dict" - dict
    "Cmd" - Cmd object
    "list:str" - list of strings
    "list:int" - list of integers
    "list:Cmd" - list of Cmd objects

    Validations depend on the type. For strings, the validator is a regular expression. For ints, the min and max values are specified.

    The node metaclass generates a setter/getter for each attribute. This keeps the schema easy to read and maintain.
    """

    ATTRS = {}

    def __iter__(self):
        """Enable cast self to dict.

        The dict contains the node's attributes, as specified in ATTRS, and their values. It does not contain attributes whose values are None or empty.
        """
        for key in self.ATTRS:
            value = getattr(self, key)()
            if value is None or value == [] or value == {}:
                continue

            # Cast Cmd objects as dicts. Their own __iter__ method will handle
            # the rest.
            if type(value) == list:
                if all(type(x).__name__ == "Cmd" for x in value):
                    value = [dict(x) for x in value]
            elif type(value).__name__ == "Cmd":
                value = dict(value)

            yield key, value

    @classmethod
    def validate_int(cls, name, *args, **kwargs):
        """Validate an int argument."""
        for arg in args:
            if not type(arg).__name__ == "int":
                raise TypeError("Value '{}' for '{}' must be an int".format(arg, name))
            if "validator" in kwargs:
                if "min" in kwargs["validator"] and arg < kwargs["validator"]["min"]:
                    raise ValueError(
                        "Value '{}' for '{}' must be at least '{}'".format(
                            arg, name, kwargs["validator"]["min"]
                        )
                    )
                if "max" in kwargs["validator"] and arg > kwargs["validator"]["max"]:
                    raise ValueError(
                        "Value '{}' for '{}' must be at most '{}'".format(
                            arg, name, kwargs["validator"]["max"]
                        )
                    )

    @classmethod
    def validate_string(cls, name, *args, **kwargs):
        """Validate a string argument."""
        for arg in args:
            if not type(arg).__name__ == "str":
                raise TypeError(
                    "Value '{}' for '{}' must be a string".format(arg, name)
                )
            if "validator" in kwargs and not kwargs["validator"].match(arg):
                raise ValueError(
                    "Value '{}' for '{}' must match {}".format(
                        arg, name, kwargs["validator"]
                    )
                )

    @classmethod
    def validate_cmd(cls, name, *args, **kwargs):
        """Validate a Cmd argument."""
        for arg in args:
            if not type(arg).__name__ == "Cmd":
                raise TypeError(
                    "Value '{}' for '{}' must be type Cmd".format(repr(arg), name)
                )
        # No need to validate command format here as it is done when the
        # command is instantiated.

    @classmethod
    def validate_dict(cls, name, *args, **kwargs):
        """Validate a dict argument."""
        for arg in args:
            if not type(arg).__name__ == "dict":
                raise TypeError("Value '{}' for '{}' must be a dict".format(arg, name))
        if "validator" in kwargs:
            valid_keys = kwargs["validator"]["keys"]
            for arg in args:
                for key in arg:
                    if key not in valid_keys:
                        raise ValueError(
                            "Key '{}' in '{}' must be one of {}".format(
                                key, name, valid_keys
                            )
                        )

    @classmethod
    def validate_bool(self, name, *args, **kwargs):
        """Validate a bool argument."""
        for arg in args:
            if not type(arg).__name__ == "bool":
                raise TypeError("Value '{}' for '{}' must be a bool".format(arg, name))
          