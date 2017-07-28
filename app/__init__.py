from .restplus import api
from flask import Flask
from instance.config import app_config
from .bucket.views_bucket import bucket
from .models import db
from .auth.views_auth import auth

def create_app(config_name):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(app_config[config_name])
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)
    api.init_app(app)



    return app
