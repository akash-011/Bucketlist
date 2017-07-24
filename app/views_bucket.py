from app import api
from flask_restplus import Resource, fields
from .models import Bucketlist, db
from flask import request


bucket = api.namespace('bucketlists', description= "Welcome")


buckett = api.model('Buckett', {
        'id': fields.Integer(required=True,readOnly=True),
        'name': fields.String(required=True ,description='This is the name of the bucketlist'),
        'date_created': fields.DateTime,
        'date_modified': fields.DateTime,
})

bucket_create = api.model('create_bucket',{
    'name': fields.String(required=True),


})


@bucket.route('/')
class Bucketlists(Resource):

    @api.expect(bucket_create)
    @api.marshal_with(buckett)
    def post(self):
        name = request.json['name']
        bucketlist = Bucketlist(name = name)
        bucketlist.save()
        return bucketlist, 201

    @api.marshal_with(buckett)
    def get(self):
        bucketlists = Bucketlist.query.all()
        return bucketlists, 200



@bucket.route('/<int:id>')
class BucketManipulation(Resource):

    @api.marshal_with(buckett)
    def get(self,id):
        bucket_list = Bucketlist.query.filter_by(id=id).first()
        if not bucket_list:
            abort(404)
        return bucket_list, 200

    def delete(self,id):
        bucket_list = Bucketlist.query.filter_by(id=id).first()
        if not bucket_list:
            abort(404)
        bucket_list.delete()
        return{
        'Message': "Bucket list deleted "
        }, 200
