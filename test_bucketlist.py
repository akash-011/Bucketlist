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
        self.assertEqual(res.status_code,200)
        self.assertIn('Go to Old trafford', str(res.data))

    def test_get_bucketby_id(self):
        bucket_post = self.client().post('/bucketlists/', data =json.dumps(self.bucketlist), headers={'content-type': 'application/json'})
        result = self.client().get('/bucketlists/1', headers = {'Accept': 'application/json'})
        self.assertEqual(result.status_code,200)
        self.assertIn('Go to Old trafford',str(result.data))

    def test_bucketlist_delete(self):
        bucket_post = self.client().post('/bucketlists/', data =json.dumps(self.bucketlist), headers={'content-type': 'application/json'})
        result = self.client().delete('/bucketlists/1', headers = {'Accept': 'application/json'})
        self.assertEqual(result.status_code,200)


    def test_bucketlist_update(self):
        bucket_post = self.client().post('/bucketlists/', data =json.dumps(self.bucketlist), headers={'content-type': 'application/json'})
        new_data = {'name': 'Go to London'}
        put_req = self.client().put('/bucketlists/1',data=json.dumps(new_data),headers={'content-type': 'application/json'})
        result = self.client().get('bucketlists/1',headers={'content-type': 'application/json'})
        self.assertIn('Go to London', str(result.data))



    def tearDown(self):

        with self.app.app_context():
            db.session.remove()
            db.drop_all()
