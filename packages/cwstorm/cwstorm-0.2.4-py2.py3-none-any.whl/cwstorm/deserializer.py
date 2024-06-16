import json
import logging

from cwstorm.dsl.cmd import Cmd
from cwstorm.dsl.task import Task
from cwstorm.dsl.upload import Upload
from cwstorm.dsl.job import Job

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

def create_job(data):
    j = Job(data.get('id'))
    j.comment(data.get('comment', 'No comment'))
    j.author(data.get('author', 'No author'))
    j.project(data.get('project', 'No project'))
    j.location(data.get('location', ""))
    j.schema_version(data.get('schema_version', '1.0.0'))
    j.metadata(data.get('metadata', {}))
    return j

def create_task(data):
    t = Task(data.get('id'))
    for cmd in data.get('commands', []):  # Use a default empty list if 'commands' is not present
        t.push_commands(Cmd(*cmd.get('argv', [])))  # Use a default empty list if 'argv' is not present
    t.env(data.get('env' , {}))
    t.initial_state(data.get('initial_state', 'HOLD'))
    t.hardware(data.get('hardware', 'No hardware'))
    t.preemptible(data.get('preemptible', True))
    for pkg in data.get('packages', []):  # Use a default empty list if 'packages' is not present
        t.push_packages(pkg)
    t.lifecycle(data.get('lifecycle', {}))
    t.attempts(data.get('attempts', 1))
    t.output_path(data.get('output_path'))
    return t

def create_upload(data):
    u = Upload(data.get('id'))
    for file_info in data.get('files', []):  # Use a default empty list if 'files' is not present
        u.push_files(file_info)
    u.initial_state(data.get('initial_state'))
    return u


# Function to deserialize JSON data
def deserialize(dikt):
    nodes = {}
    job = None
    # Create nodes
    for node_info in dikt['nodes']:
        data = node_info['data']
        node_type = data['type']
        node_id = data['id']

        if node_type == 'job':
            node = create_job(data)
            job = node
        elif node_type == 'task':
            node = create_task(data)
        elif node_type == 'upload':
            node = create_upload(data)
        else:
            logger.error("Skipping unknown node type: %s", node_type)
        nodes[node_id] = node
    
    # Create edges
    for edge_info in dikt['edges']:
        data = edge_info['data']
        source_node = nodes[data['source']]
        target_node = nodes[data['target']]
        target_node.add(source_node)
    
    return job
