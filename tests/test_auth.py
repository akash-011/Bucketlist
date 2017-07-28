import unittest
import json
from app import create_app
from app.models import db

class AuthTestCase(unittest.TestCase):

    def setUp(self):

        self.app = create_app(config_name='testing')
        self.client = self.app.test_client
        self.user_data = {
            'user_email': 'test@test.com',
            'password': 'test123'
        }

        with self.app.app_context():

            #db.session.close()
            db.drop_all()
            db.create_all()


    def test_registration(self):
        resp = self.client().post('/auth/register', data =json.dumps(self.user_data), headers={'content-type': 'application/json'})
        result = json.loads(resp.data)
        self.assertIn("Registration Succesful", result['message'])
        self.assertEqual(resp.status_code,201)

    def test_already_registered(self):
        resp = self.client().post('/auth/register', data =json.dumps(self.user_data), headers={'content-type': 'application/json'})
        result = self.client().post('/auth/register', data =json.dumps(self.user_data), headers={'content-type': 'application/json'})
        result_mess = json.loads(result.data)
        self.assertEqual(result.status_code,400)
        self.assertIn("User already exists",result_mess['message'])



    def tearDown(self):

        with self.app.app_context():
            db.session.remove()
            db.drop_all()
