from .restplus import api
from flask_sqlalchemy import SQLAlchemy
from flask import Flask
from instance.config import app_config
from .bucket import hello_name

db = SQLAlchemy()

def create_app(config_name):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(app_config[config_name])
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)
    api.add_namespace(hello_name)
    api.init_app(app)



    return app
