
from flask import current_app
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy
import jwt
from datetime import datetime, timedelta

db = SQLAlchemy()

class User(db.Model):

    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key = True)
    user_email = db.Column(db.String(50), nullable=False, unique=True)
    password = db.Column(db.String())
    bucketlists = db.relationship('Bucketlist', order_by='Bucketlist.id', cascade="all, delete-orphan")


    def __init__(self,user_email,password):
        self.user_email = user_email
        self.password = Bcrypt().generate_password_hash(password).decode()

    def password_validity(self,password):

        return Bcrypt().check_password_hash(self.password,password)

    def save(self):
        db.session.add(self)
        db.session.commit()

    def generate_token(self , user_id):

        try:
            payload = {
                'exp' : datetime.utcnow() + timedelta(minutes=5),
                'iat' : datetime.utcnow(),
                'sub' : user_id
            }
            jwt_string = jwt.encode(
                payload,
                current_app.config.get('SECRET'),
                algorithm='HS256'
            )
            return jwt_string

        except Exception as e:
            return str(e)



    def decode_token(token):

        try:
            payload = jwt.decode(token,current_app.config.get('SECRET'))
            return payload['sub']
        except jwt.ExpiredSignatureError:
            return "Expired Token , Please Log in"
        except jwt.InvalidTokenError:
            return "Please Log in or Register"




class Bucketlist(db.Model):

    __tablename__ = "bucketlists"

    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(255))
    date_created = db.Column(db.DateTime, default = db.func.current_timestamp())
    date_modified = db.Column(db.DateTime, default = db.func.current_timestamp(), onupdate= db.func.current_timestamp())
    created_by = db.Column(db.Integer, db.ForeignKey(User.id))

    def __init__(self,name,created_by):
        self.name = name
        self.created_by = created_by

    def save(self):
        db.session.add(self)
        db.session.commit()

    @staticmethod
    def get_all(user_id):
        return Bucketlist.query.filter_by(created_by=user_id)

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def __repr__(self):
        return "<Bucketlist: {}>".format(self.name)

class Bucketitems(db.Model):

    __tablename__ = "bucketitems"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    date_created = db.Column(db.DateTime, default = db.func.current_timestamp())
    date_modified = db.Column(db.DateTime, default = db.func.current_timestamp(), onupdate= db.func.current_timestamp())
    done = db.Column(db.Boolean, default=False)
    bucketlist_id = db.Column(db.Integer, db.ForeignKey(Bucketlist.id))

    def __init__(self,name,bucketlist_id):
        self.name = name
        self.bucketlist_id = bucketlist_id


    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def __repr__(self):
        return '<Bucketlist Item {}>'.format(self.name)
