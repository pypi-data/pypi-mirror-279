from cwstorm.dsl.node import Node
import re


class Cmd(Node):
    """
    Cmd.
    
    A Cmd represents a single command line to be executed. Tasks hold a list of commands, and Cmd arguments are held in a list. Lists of commands in a task run in serial.
    """
    ATTRS = {
        "argv": {
            "type": "list:str",
            "validator": re.compile(r"^[a-zA-Z0-9_@,\-\.\/\s%:*?<>$()+%'\"]+$", re.IGNORECASE),
            "required": True
        },

    }

    def __init__(self, *args):
        self.argv(*args)
