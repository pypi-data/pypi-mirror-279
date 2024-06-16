import os
import click
import importlib
import json
import yaml
import sys
from cwstorm.version import VERSION
from cwstorm.serializers import default
from cwstorm import validator
import textwrap
import re

from cwstorm.dsl.cmd import Cmd
from cwstorm.dsl.task import Task
from cwstorm.dsl.upload import Upload
from cwstorm.dsl.job import Job
from cwstorm.dsl.dag_node import DagNode

import markdown
import io
import tempfile
import webbrowser

from cwstorm import __schema_version__

import traceback


PURE = """
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/purecss@3.0.0/build/pure-min.css" integrity="sha384-X38yfunGUhNzHpBaEBsWLO+A0HDYOQi8ufWDkZ0k9e0eXz/tH3II7uKZ9msv++Ls" crossorigin="anonymous">
<meta name="viewport" content="width=device-width, initial-scale=1">
"""

EXAMPLES_FOLDER = os.path.join(os.path.dirname(os.path.realpath(__file__)), "examples")
EXAMPLE_MODULES_PREFIX = "cwstorm.examples."
GET_JOB_FUNCTION_NAME = "get_job"


EXAMPLE_FILES = os.listdir(EXAMPLES_FOLDER)
MODULE_FILES = [
    file for file in EXAMPLE_FILES if file.endswith(".py") and not file.startswith("__")
]
MODULE_NAMES = [file[:-3] for file in MODULE_FILES]  # Remove the .py extension


def _wrap_text(text, width):
    return "\n".join(textwrap.wrap(text, width=width))


########################### MAIN #################################
@click.group(invoke_without_command=True)
@click.pass_context
@click.option("-v", "--version", is_flag=True, help="Print the version and exit.")
def main(ctx, version):
    """Storm Command-line interface."""
    if not ctx.invoked_subcommand:
        if version:
            click.echo(VERSION)
            ctx.exit()
        click.echo(ctx.get_help())
        ctx.exit()


SERIALIZE_HELP = """The structure of serialized DAG. 

default: is a list of nodes and a list of edges. The edges contain source and target pointers to node labels. This is the simplest and easiest to understand. It is also understood by the UI.
"""

FORMAT_HELP = """The output format. JSON and YAML are implemented. Pretty is a pretty-printed JSON.
"""

EXAMPLE_HELP = """The example job to serialize. The examples are in the storm/examples folder. The examples are python modules that contain a function called get_job that returns a job object.
"""


########################### SERIALIZE #############################
@main.command()
@click.option(
    "-f",
    "--fmt",
    "--format",
    help=FORMAT_HELP,
    default="json",
    type=click.Choice(choices=["json", "pretty", "yaml"], case_sensitive=False),
)
@click.option(
    "-x",
    "--example",
    help=EXAMPLE_HELP,
    default="simple",
    type=click.Choice(choices=MODULE_NAMES + ["all"], case_sensitive=True),
)
@click.argument(
    "output",
    required=False,
    type=click.Path(file_okay=False, dir_okay=True, resolve_path=True),
)
def serialize(fmt, example, output):
    """
    Serialize a job to json or yaml.

    Examples:

    # Output json to stdout.
    storm serialize -f json -x frames

    # Output json to a file for visualization.
    storm serialize -f json -x frames ~/Desktop

    # Output yaml to a file for using the the assex job example.
    storm serialize -f yaml -s storm  -x assex ~/Desktop

    """
    if example == "all":
        for example in MODULE_NAMES:
            _serialize(fmt, example, output)
    else:
        _serialize(fmt, example, output)


def _serialize(fmt, example, output):
    module_name = EXAMPLE_MODULES_PREFIX + example
    module = importlib.import_module(module_name)
    storm_script = getattr(module, GET_JOB_FUNCTION_NAME)
    job = storm_script()

    serialized = default.serialize(job)
    # Determine the output method (stdout or file)
    if output:
        ext = {
            "json": "json",
            "pretty": "json",
            "yaml": "yml",
        }
        fh = open(os.path.join(output, f"{example}.{ext[fmt]}"), "w", encoding="utf-8")
    else:
        fh = sys.stdout
    try:
        if fmt == "json":
            json.dump(serialized, fh)
        elif fmt == "pretty":
            json.dump(serialized, fh, indent=3)
        elif fmt == "yaml":
            yaml.dump(serialized, fh)
        else:
            raise ValueError(f"Unknown format: {fmt}")
    finally:
        # Only close the file if we're not writing to stdout
        if output:
            fh.close()


# storm serialize -x all  /Volumes/xhf/dev/cio/cioapp/public/graphs/ done


########################### VALIDATE #############################


@main.command()
@click.option(
    "-f",
    "--fmt",
    "--format",
    help=FORMAT_HELP,
    default="html",
    type=click.Choice(choices=["markdown", "html"], case_sensitive=False),
)
@click.argument("infile", nargs=1, type=click.Path(exists=True, resolve_path=True))
def validate(fmt, infile):
    """
    Validate a JSON file.

    storm validate /path/to/file.json


    """

    md = _as_markdown(infile)
    if fmt == "markdown":
        print(md)
    else:  # fmt == "html":
        html = markdown.markdown(md, extensions=["markdown.extensions.tables"])
        html = decorate(html)

        with tempfile.NamedTemporaryFile(mode="w", suffix=".html", delete=False) as f:
            f.write(html)
            webbrowser.open("file://" + f.name, new=2)


def _as_markdown(infile):
    stream = io.StringIO()
    stream.write(f"# Storm Validation Report:\n\n{infile}")

    with open(infile, "r", encoding="utf-8") as fh:
        data = json.load(fh)
        try:
            validation = validator.validate(data)
        except Exception:
            tb_lines = traceback.format_exc().splitlines()
            stream.write("\n\n".join(["```python"] + tb_lines + ["```"]))
            return stream.getvalue()

    stream.write("\n\n## Input Counts\n\n")
    stream.write("| Type | Count |\n")
    stream.write("|------|-------|\n")
    for key, value in validation["input_info"]:
        stream.write(f"| {key} | {value} |\n")

    stream.write("\n\n## Deserialized Job Info\n\n")
    stream.write("| Param | Value | Valid |\n")
    stream.write("|-------|-------|-------|\n")
    for key, value, valid in validation["job_info"]:
        stream.write(f"| {key} | {value} | {valid} |\n")
    result = stream.getvalue()
    stream.close()
    return result


########################### DISPLAY #############################
@main.command()
@click.option(
    "-f",
    "--fmt",
    "--format",
    help=FORMAT_HELP,
    default="html",
    type=click.Choice(choices=["markdown", "html"], case_sensitive=False),
)
def schema(fmt):
    """
    Display the schema.
    
    Shows the attributes of classes in the DSL in a web page or as markdown.
    """
    if fmt == "markdown":
        display_schema_markdown(DagNode, Job, Task, Cmd, Upload)
    elif fmt == "html":
        display_schema_html(DagNode, Job, Task, Cmd, Upload)


def display_schema_markdown(*klasses):
    stream = io.StringIO()
    stream.write(
        "# Storm DSL Schema - Version {}\n\n".format(__schema_version__)
    )

    for klass in klasses:
        class_schema_to_stream(klass, stream)
    print(stream.getvalue())


def display_schema_html(*klasses):
    stream = io.StringIO()
    stream.write(
        "# Storm DSL Schema - Version {}\n\n".format(__schema_version__)
    )

    for klass in klasses:
        class_schema_to_stream(klass, stream)
    html = markdown.markdown(
        stream.getvalue(), extensions=["markdown.extensions.tables"]
    )
    html = decorate(html)
    stream.close()
    with tempfile.NamedTemporaryFile(mode="w", suffix=".html", delete=False) as f:
        f.write(html)
        webbrowser.open("file://" + f.name, new=2)


def class_schema_to_stream(klass, stream):
    class_name = klass.__name__
    base_class = klass.__bases__[0].__name__
    docstring_paragraphs = re.split(r"\n\s*\n", klass.__doc__) if klass.__doc__ else []
    docstring_paragraphs = [p.strip() for p in docstring_paragraphs]
    class_description = (
        "\n\n".join(docstring_paragraphs[1:])
        if len(docstring_paragraphs) > 1
        else "No description available."
    )

    desc = f"## Class: {class_name} ({base_class})\n\n#### Description:\n{class_description}\n\n"
    stream.write(desc)

    if len(klass.ATTRS) == 0:
        stream.write("\n\n")
        return
    headers = ["Name", "Type", "Default", "Required", "Validator"]
    rows = [format_attr(name, attr) for name, attr in klass.ATTRS.items()]
    column_widths = [max(len(str(item)) for item in col) for col in zip(headers, *rows)]
    row_format = (
        "| " + " | ".join("{:<" + str(width) + "}" for width in column_widths) + " |"
    )
    stream.write(row_format.format(*headers))
    stream.write("\n")
    stream.write("|-" + "-|-".join("-" * width for width in column_widths) + "-|")
    stream.write("\n")
    for row in rows:
        stream.write(row_format.format(*row))
        stream.write("\n")
    stream.write("\n\n")
    stream.write("---\n\n")


def format_attr(name, attr):
    # Format type
    type_str = (
        attr["type"]
        .replace("list:", "List of ")
        .replace("int", "Integer")
        .replace("bool", "Boolean")
        .replace("str", "String")
        .replace("dict", "Dictionary")
    )

    # Format default value
    default_str = str(attr.get("default", ""))
    
    required_str = "Yes" if attr.get("required", False) else "No"

    # Format validator
    validator_str = ""
    if "validator" in attr:
        if isinstance(attr["validator"], re.Pattern):
            validator_str = f"Regex: {attr['validator'].pattern}"

        else:
            validator_str = str(attr["validator"])
        validator_str = validator_str.replace("|", "\\|")
        validator_str = f"`{validator_str}`"
    return [name, type_str, default_str, required_str, validator_str]


def decorate(html):
    html = html.replace("<table>", '<table class="pure-table pure-table-bordered">')
    html = '<html><head>{}</head><body style="margin: 2em;width=800px">{}</body></html>'.format(
        PURE, html
    )
    return html
