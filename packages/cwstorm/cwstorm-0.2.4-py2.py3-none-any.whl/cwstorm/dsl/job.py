import re
import os
import platform
from cwstorm.dsl.dag_node import DagNode
from datetime import datetime
from cwstorm import __schema_version__

class Job(DagNode):
    """Job node.
    
    There's exactly one job node for each workflow. The job node summarizes the workflow and its status once tasks start running.
    """

    ATTRS = {
        "comment": {
            "type": "str",
            "validator": re.compile(r'^[_a-z0-9 ,.!?\'"]+$', re.IGNORECASE),
            "required": False
        },
        "project": {
            "type": "str",
            "validator": re.compile(r"^[a-z0-9_\-\.\s]+$", re.IGNORECASE),
            "required": True
        },
        "author": {
            "type": "str",
            "validator": re.compile(r"^[a-z\s]+$", re.IGNORECASE),
            "required": False
        },
        "location": {
            "type": "str",
            "validator": re.compile(r'^(?:[a-z][a-z0-9]*$|([0-9A-Fa-f]{2}[:-]){5}([0-9A-Fa-f]{2})$|^$)', re.IGNORECASE),
            "required": False
            
        },
        "metadata": {"type": "dict",
            "required": False
        },
        "schema_version": {
            "type": "str",
            "validator": re.compile(r"^\d{1,2}\.\d{1,2}.\d{1,2}$"),
            "default": __schema_version__,
            "required": True
            
        }
    }
    
    def is_original(self, parent=None):
        """Always true."""
        return True

    def is_reference(self, parent):
        """Always false."""
        return False

    def __init__(self, *args, **kw):
        super().__init__(*args, **kw)
        self.schema_version(self.ATTRS["schema_version"]["default"])
        self.author(self.get_username())

    @staticmethod
    def get_username():
        """Return the username of the current user."""
        result =  os.environ.get("USERNAME") if platform.system() == "Windows" else os.environ.get("USER")
        if not result:
            result =   os.environ.get("CIRCLE_USERNAME")
        if not result:
            result =  "unknown"
        return result
