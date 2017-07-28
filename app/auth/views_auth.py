from app import api
from flask_restplus import Resource, fields
from ..models import db, User
from flask import request, abort


auth = api.namespace('auth',description="User Registration and Authorization")

register = api.model('register',{
    'id' : fields.Integer(required=True,readOnly=True),
    'user_email' : fields.String(required=True),
    'password' : fields.String(required=True),
})


create_user = api.model('create_user',{
    'user_email' : fields.String(required=True),
    'password' : fields.String(required=True),
})


@auth.route('/register')
class Register(Resource):

    @api.expect(create_user)
    def post(self):
        data = request.get_json(force=True)
        new_email = data.get('user_email')
        new_password = data.get('password')

        if not User.query.filter_by(user_email=new_email).first():
            try:
                new_user = User(new_email,new_password)
                new_user.save()
                response = {'message': "Registration Succesful"}
                return response, 201
            except Exception as e:
                response = {'message': str(e)}
                return response, 401
        response = {'message': "User already exists"}
        return response , 400


@auth.route('/login')
class Login(Resource):

    @api.expect(create_user)
    def post(self):

        data = request.get_json(force=True)
        email = data.get('user_email')
        password = data.get('password')

        find_user = User.query.filter_by(user_email=email).first()
        if find_user and find_user.password_validity(password):
            token = find_user.generate_token(find_user.id)
            if token:
                response = {
                    'message': "Login Succesful",
                    'token': token.decode()
                }
                return response, 200
            else:
                response = {
                    'message': "Login Unsuccesful",
                }
                return response , 401
