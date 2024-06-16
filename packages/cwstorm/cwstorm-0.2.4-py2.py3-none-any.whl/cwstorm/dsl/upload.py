from cwstorm.dsl.dag_node import DagNode

# from cwstorm.dsl.cmd import Cmd
import re


class Upload(DagNode):
    """Upload node.

    Uploads contain lists of filepaths. They are a special kind of task and can be added anywhere a Task can be added.
    """

    ATTRS = {
        "files": {
            "type": "list:dict",
            "required": True,
            "validator": {"keys": ["path", "size", "md5"]},
        },
        "initial_state": {
            "type": "str",
            "validator": re.compile(r"^(HOLD|START)$"),
            "default": "HOLD",
            "required": True,
        }
    }


    def __init__(self, name=None):
        """Init the task."""

        super().__init__(name)
        self.initial_state(self.ATTRS["initial_state"]["default"])



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
