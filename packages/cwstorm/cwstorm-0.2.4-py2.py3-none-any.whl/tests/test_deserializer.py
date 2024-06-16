import unittest
from unittest.mock import patch

from cwstorm.deserializer import create_job, create_task, create_upload, deserialize
from cwstorm.dsl.dag_node import DagNode


class TestJobCreation(unittest.TestCase):
    def setUp(self):
        self.job_data = {
            'id': 'job1',
            'comment': 'Test job',
            'project': 'ProjectX',
            'status': 'WAITING',
            'location': 'Location',
            'schema_version': '1.0.0',
            'author': 'AuthorZ',
            'email': 'author@example.com',
            'metadata': {'key': 'value'}
        }
    
    def tearDown(self):
        DagNode.reset()

    def test_create_job(self):
        job = create_job(self.job_data)
        self.assertEqual(job.name(), self.job_data['id'])
        self.assertEqual(job.comment(), self.job_data['comment'])
        self.assertEqual(job.project(), self.job_data['project'])
        self.assertEqual(job.location(), self.job_data['location'])
        self.assertEqual(job.schema_version(), self.job_data['schema_version'])
        self.assertEqual(job.author(), self.job_data['author'])
        self.assertEqual(job.metadata(), self.job_data['metadata'])
        
 
class TestTaskCreation(unittest.TestCase):
    def setUp(self):
        self.task_data = {
            'id': 'task1',
            'commands': [
                {'argv': ['echo', 'Hello World']}, 
                {'argv': ['echo', 'Goodbye Cruel World']}
            ],
            'env': {'PATH': '/usr/bin'},
            'initial_state': 'HOLD',
            'hardware': 'x86_64',
            'lifecycle':  {'minsec': 30, 'maxsec': 1500},
            'attempts': 3,
            'output_path': '/tmp/output',
            'status': 'WAITING'
        }
        
    def tearDown(self):
        DagNode.reset()

    def test_create_task(self):
        task = create_task(self.task_data)
        self.assertEqual(task.name(), self.task_data['id'])
        self.assertEqual(len(task.commands()), 2)
        self.assertEqual(task.env(), self.task_data['env'])
        self.assertEqual(task.initial_state(), self.task_data['initial_state'])
        self.assertEqual(task.hardware(), self.task_data['hardware'])
        self.assertEqual(task.lifecycle(), self.task_data['lifecycle'])
        self.assertEqual(task.attempts(), self.task_data['attempts'])
        self.assertEqual(task.output_path(), self.task_data['output_path'])
        
        # ... continue for all fields

class TestUploadCreation(unittest.TestCase):
    def setUp(self):
        self.upload_data = {
            'id': 'upload1',
            'files': [
                {'path': '/tmp/file.txt', 'size': 1024},
                {'path': '/tmp/other.txt', 'size': 2048}
            ],
            'initial_state': 'START',
            'status': 'SUCCESS'
        }
        
    def tearDown(self):
        DagNode.reset()

    def test_create_upload(self):
        upload = create_upload(self.upload_data)
        self.assertEqual(upload.name(), self.upload_data['id'])
        self.assertEqual(len(upload.files()), 2)
        self.assertEqual(upload.initial_state(), self.upload_data['initial_state'])
        

class TestDeserialization(unittest.TestCase):
    def setUp(self):
        self.deserialized_data = {
            'nodes': [
                {'data': {'type': 'job', 'id': 'job1'}},
                {'data': {'type': 'task', 'id': 'task1', "output_path": "/media/","initial_state": "HOLD"}},
                {'data': {'type': 'upload', 'id': 'upload1',"initial_state": "HOLD"}}
            ],
            'edges': [
                {'data': {'source': 'task1', 'target': 'job1'}},
                {'data': {'source': 'upload1', 'target': 'job1'}}
            ]
        }
        
    def tearDown(self):
        DagNode.reset()
    
    @patch('cwstorm.deserializer.create_job')
    @patch('cwstorm.deserializer.create_task')
    @patch('cwstorm.deserializer.create_upload')
    def test_deserialize(self, mock_create_upload, mock_create_task, mock_create_job):
        job = deserialize(self.deserialized_data)
        mock_create_job.assert_called_once()
        mock_create_task.assert_called_once()
        mock_create_upload.assert_called_once()
        

    def test_deserialize_connects_nodes(self):
        job = deserialize(self.deserialized_data)
        self.assertEqual(len(job.children), 2)
        self.assertEqual(job.children[0].name(), 'task1')
        self.assertEqual(job.children[1].name(), 'upload1')

if __name__ == '__main__':
    unittest.main()
