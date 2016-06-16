from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import flask_restless

app = Flask(__name__)
app.config.from_object('config')
db = SQLAlchemy(app)

from app import views, models

manager = flask_restless.APIManager(app, flask_sqlalchemy_db=db)
manager.create_api(models.Name, methods=['GET'])
manager.create_api(models.Set, methods=['GET'], results_per_page=0)
