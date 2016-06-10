# Runs both locally (using python index.py) and on WebFaction

import random
import sys
import os

from flask_sqlalchemy import SQLAlchemy

CURRENT_FILE = os.path.abspath(__file__)
CURRENT_DIR = os.path.dirname(CURRENT_FILE)
PROJECT_DIR = os.path.dirname(CURRENT_DIR)

# For WebFaction, should be ignored locally
sys.path.append(PROJECT_DIR + '/virtualenv/lib/python3.5/site-packages/')
sys.path.append(PROJECT_DIR + '/src/')
sys.path.append(PROJECT_DIR + '/src/app/')

from app import app

db = SQLAlchemy(app)

from app.models import Name, NameFrequency

def create_test_data():

    # Create the tables, if not done yet
    try:
        db.create_all()
    except:
        pass

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

if __name__ == '__main__':
    create_test_data()
