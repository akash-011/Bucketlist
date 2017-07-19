from app import api
from flask_restplus import Resource


hello_name = api.namespace('hello', description= "Welcome")

@hello_name.route('/')
class HelloWorld(Resource):
    def get(self):
        return {'hello': 'world'}
