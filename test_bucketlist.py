import os
import unittest
import json
from app import create_app
from app.models import db


class BUcketlistTestCase(unittest.TestCase):

    def setUp(self):

        self.app = create_app(config_name = "testing")
        self.client = self.app.test_client
        self.bucketlist = {'name': 'Go to Old trafford'}

        with self.app.app_context():
            db.create_all()



    def test_create_bucketlist(self):
        result = self.client().post('/bucketlists/', data =json.dumps(self.bucketlist), headers={'content-type': 'application/json'})
        self.assertEqual(result.status_code, 201)
        self.assertIn("Go to Old trafford", str(result.data))


    def test_getall_bucketists(self):
        bucket_post = self.client().post('/bucketlists/', data =json.dumps(self.bucketlist), headers={'content-type': 'application/json'})
        self.assertEqual(bucket_post.status_code,201)
        res = self.client().get('/bucketlists/', headers = {'Accept': 'application/json'})
        self.assertEqual(result.status_code,200)
        self.assertIn('Go to Old trafford', str(res.data))

    def tearDown(self):

        with self.app.app_context():
            db.session.remove()
            db.drop_all()
