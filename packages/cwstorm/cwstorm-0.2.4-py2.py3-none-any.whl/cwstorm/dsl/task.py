from cwstorm.dsl.dag_node import DagNode

# from cwstorm.dsl.cmd import Cmd
import re


class Task(DagNode):
    """Task node.

    Tasks contain commands. They may be added to other Tasks as children or to the Job. A task may be the child of many parents.
    """

    ATTRS = {
        "commands": {"type": "list:Cmd", "required": True},
        "hardware": {
            "type": "str",
            "validator": re.compile(r"^[a-z0-9_\-\.\s]+$", re.IGNORECASE),
            "required": True,
        },
        "preemptible": {"type": "bool", "default": True, "required": True},
        "env": {"type": "dict", "required": False},
        "lifecycle": {
            "type": "dict",
            "required": False,
            "validator": {"keys": ["minsec", "maxsec"]},
        },
        "attempts": {
            "type": "int",
            "validator": {"min": 1, "max": 10},
            "default": 1,
            "required": True,
        },
        "initial_state": {
            "type": "str",
            "validator": re.compile(r"^(HOLD|START)$"),
            "default": "HOLD",
            "required": True,
        },
        "output_path": {"type": "str", "default":"/tmp", "required": True},
        "packages": {
            "type": "list:str",
            "required": False, 
            "validator": re.compile(r"^[a-fA-F0-9]{32}$"),
        },
    }

    def __init__(self, name=None):
        """Init the task."""

        super().__init__(name)
        self.preemptible(self.ATTRS["preemptible"]["default"])
        self.attempts(self.ATTRS["attempts"]["default"])
        self.initial_state(self.ATTRS["initial_state"]["default"])
        self.output_path(self.ATTRS["output_path"]["default"])

    def is_original(self, parent=None):
        """True if the parent is the first parent or there are no parents."""
        if not parent:
            return True
        if not self.parents:
            return True
        if self.parents[0] == parent:
            return True
        return False

    def is_reference(self, parent):
        """True if the parent is a parent and not the first parent."""
        return (
            parent
            and self.parents
            and len(self.parents) > 1
            and parent != self.parents[0]
            and parent in self.parents
        )
