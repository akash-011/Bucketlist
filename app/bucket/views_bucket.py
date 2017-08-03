from app import api
from flask_restplus import Resource, fields
from ..models import Bucketlist, db, User
from flask import request, abort


bucket = api.namespace('bucketlists', description= "Welcome")


buckett = api.model('Buckett', {
        'id': fields.Integer(required=True,readOnly=True),
        'name': fields.String(required=True ,description='This is the name of the bucketlist'),
        'date_created': fields.DateTime,
        'date_modified': fields.DateTime,
        'created_by': fields.Integer,
})

bucket_create = api.model('create_bucket',{
    'name': fields.String(required=True),


})


@bucket.route('/')
class Bucketlists(Resource):

    @api.header('Authorization', 'JWT Token', required=True)
    @api.expect(bucket_create)
    @api.marshal_with(buckett)
    def post(self):
        token = request.headers.get('Authorization')
        if token:
            user_id = User.decode_token(token)

            if not isinstance(user_id,str):
                name = request.json['name']
                bucketlist = Bucketlist(name = name,created_by=user_id)
                bucketlist.save()
                return bucketlist, 201
            abort (401, user_id)

    @api.header('Authorization', 'JWT Token', required=True)
    @api.marshal_list_with(buckett)
    def get(self):
        token = request.headers.get('Authorization')
        if token:
            user_id = User.decode_token(token)
            if not isinstance(user_id, str):
                bucketlists = Bucketlist.query.filter_by(created_by=user_id).all()
                return bucketlists, 200
            abort(401,user_id)


@bucket.route('/<int:id>')
class BucketManipulation(Resource):

    @api.header('Authorization', 'JWT Token', required=True)
    @api.marshal_with(buckett)
    def get(self,id):
        token = request.headers.get('Authorization')
        if token:
            user_id = User.decode_token(token)
            bucket_list = Bucketlist.query.filter_by(id=id, created_by=user_id).first()
            if not bucket_list:
                abort(404)
            return bucket_list, 200

    @api.header('Authorization', 'JWT Token', required=True)
    def delete(self,id):
        token = request.headers.get('Authorization')
        if token:
            user_id = User.decode_token(token)
            bucket_list = Bucketlist.query.filter_by(id=id, created_by=user_id).first()
            if not bucket_list:
                abort(404)
                bucket_list.delete()
                return{
                        'Message': "Bucket list deleted "
                        }, 200

    @api.header('Authorization', 'JWT Token', required=True)
    @api.expect(bucket_create)
    @api.marshal_with(buckett)
    def put(self,id):
            token = request.headers.get('Authorization')
            if token:
                user_id = User.decode_token(token)
                new_name = request.json['name']
                try:
                    bucket_list = Bucketlist.query.filter_by(id=id, created_by=user_id).first()
                    bucket_list.name = new_name
                    bucket_list.save()
                    return bucket_list, 200
                except AttributeError:
                    abort(404)
