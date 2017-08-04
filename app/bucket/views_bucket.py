from app import api
from flask_restplus import Resource, fields
from ..models import Bucketlist, db, User, Bucketitems
from flask import request, abort


bucket = api.namespace('bucketlists', description= "Welcome")

bucket_item = api.model('bucket_item',{
        'id': fields.Integer(required=True,readOnly=True),
        'name': fields.String(required=True),
        'date_created': fields.DateTime,
        'date_modified': fields.DateTime,
        'done': fields.Boolean,
})

bucket_item_update = api.model('bucket_item_update', {
    'name': fields.String(description='Name of the bucketlist item'),
    'done': fields.Boolean(description='Status of the bucketlist item')
})
buckett = api.model('Buckett', {
        'id': fields.Integer(required=True,readOnly=True),
        'name': fields.String(required=True ,description='This is the name of the bucketlist'),
        'items': fields.List(fields.Nested(bucket_item)) ,
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




@bucket.route('/<int:id>/items')
class BucketItem(Resource):

    @api.header('Authorization', 'JWT Token', required=True)
    @api.expect(bucket_create)
    @api.marshal_with(bucket_item)
    def post(self,id):

        token = request.headers.get('Authorization')
        data = request.json
        name = data.get('name')

        if token:
            user_id = User.decode_token(token)
            try:
                bucketlist = Bucketlist.query.filter_by(id=id,created_by=user_id).first()
                if not isinstance(user_id,str):
                    new_item = Bucketitems(name, id)
                    new_item.save()
                    return new_item, 201
            except AttributeError:
                abort(404, 'Bucketlist does not exist')

        else:
            abort(401)

@bucket.route('/<int:id>/items/<int:item_id>')
class BucketItemWithID(Resource):

    @api.expect(bucket_item_update)
    @api.marshal_with(bucket_item)
    @api.header('Authorization', 'JWT Token', required=True)
    def put(self,id,item_id):

        token = request.headers.get('Authorization')

        if token:
            user_id = User.decode_token(token)
            try:
                bucketlist = Bucketlists.query.filter_by(id=id,created_by=user_id).first()
                try:
                    item_update = BucketItems.query.filter_by(id=item_id)
                    try:
                        new_name = request.json['name']
                        item_update.name = new_name
                    except KeyError:
                        pass
                    try:
                        new_status = request.json['done']
                        item_update.done = new_status

                    except KeyError:
                        pass
                except AttributeError:
                    abort(404,'Bucket Item not found')

            except AttributeError:
                abort(404,'Bucketlist not found')


    @api.header('Authorization', 'JWT Token', required=True)
    def delete(self,id,item_id):

        token = request.headers.get('Authorization')

        if token:

            user_id = User.decode_token(token)
            try:
                bucketlist = Bucketlist.query.filter_by(id=id,created_by=user_id).first()
                try:
                    item_delete = Bucketitems.query.filter_by(id=item_id,bucketlist_id=bucketlist.id).first()
                    item_delete.delete()
                    response = {'message': 'Bucket item has been deleted'}
                    return response, 200
                except AttributeError:
                    abort(404,"item not found")

            except AttributeError:
                abort(404,"Bucketlist not found")
