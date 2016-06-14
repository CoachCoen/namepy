# Runs both locally (using python index.py) and on WebFaction

# On WebFaction, must be run after activating the virtualenv

import random

from app import db

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
