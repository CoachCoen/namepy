from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import flask_restless

app = Flask(__name__)
app.config.from_object('config')
db = SQLAlchemy(app)

from app import views, models

manager = flask.ext.restless.APIManager(app, flask_sqlalchemy_db=db)
manager.create_api(models.Name, methods=['GET'])
