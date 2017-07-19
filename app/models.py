from app import db
from flask_bcrypt import Bcrypt

class User(db.Model):

    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key = True)
    user_email = db.Column(db.String(50), nullable=False, unique=True)
    password = db.Column(db.String())
    buckets = db.relationship('Bucketlist', order_by='Bucketlist.id', cascade = "all, delete-orphan")

    def __init__(self,email,password):
        self.email = email
        self.password = Bcrypt().generate_password_hash(password).decode()

    def password_validity(self,password):

        return Bcrypt().check_password_hash(self.password,password)

    def save(self):
        db.session.add(self)
        db.session.commit(self)



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
        db.session.commit(self)

    @staticmethod
    def get_all():
        return Bucketlist.query.filter_by(created_by=user_id)

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def __repr__(self):
        return "<Bucketlist: {}>".format(self.name)
