# Runs both locally (using python index.py) and on WebFaction using WSGI

import random
import sys
import os

from flask_sqlalchemy import SQLAlchemy

from app import app

CURRENT_FILE = os.path.abspath(__file__)
CURRENT_DIR = os.path.dirname(CURRENT_FILE)
PROJECT_DIR = os.path.dirname(CURRENT_DIR)

# Add project top-dir to path (since it has no __init__.py)
# sys.path.append(PROJECT_DIR + '/src/')

# Add virtualenv to path - only for WebFaction, should be ignored locally
sys.path.append(PROJECT_DIR + '/virtualenv/lib/python3.5/site-packages/')

db = SQLAlchemy(app)

from app.models import Name, NameFrequency

def create_test_data():
    db.session.query(NameFrequency).delete()
    db.session.query(Name).delete()
    db.session.commit()
    for name in ('Fred', 'Sue'):
        new_name = Name(name=name)
        db.session.add(new_name)
        for year in range(1990, 1996):
            new_frequency = NameFrequency(
                name=new_name,
                year=year,
                boys_count=random.randint(50, 100),
                girls_count=random.randint(50, 100))
    db.session.commit()

# Export the Flask app object from the project as wsgi application object

if __name__ == '__main__':
    create_test_data()
