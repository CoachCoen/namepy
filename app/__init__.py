from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
import flask.ext.restless

app = Flask(__name__)
app.config.from_object('config')
db = SQLAlchemy(app)

from app import views, models

manager = flask.ext.restless.APIManager(app, flask_sqlalchemy_db=db)

# Create API endpoints, which will be available at /api/<tablename> by
# default. Allowed HTTP methods can be specified as well.
manager.create_api(models.Name, methods=['GET'])
