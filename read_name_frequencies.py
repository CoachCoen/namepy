# Runs both locally (using python index.py) and on WebFaction

# On WebFaction, must be run after activating the virtualenv

import random
import os
from os import listdir

from app import db

from app.models import Name, NameFrequency

def read_frequencies_from_file(filename, names):
    print(filename)
    year = int(filename[3:7])

    year_frequencies = {}
    for name in names:
        year_frequencies[name] = {'F': 0, 'M': 0}

    with open('raw_data/%s' % filename) as file:
        for line in file.readlines():
            try:
                name_text, sex, count = line.split(",")
            except:
                print("Couldn't parse line")
                print(line)
                print
                continue

            if name_text not in names:
                name = Name(name=name_text)
                db.session.add(name)
                db.session.commit()
                names[name_text] = name.id
                year_frequencies[name_text] = {'F': 0, 'M': 0}

            year_frequencies[name_text][sex] = int(count)

        for name, name_frequency in year_frequencies.iteritems():
            if name_frequency['F'] + name_frequency['M']:
                name_id = names[name]
                frequency_record = NameFrequency(name_id=name_id,
                    year=year,
                    boys_count=name_frequency['M'],
                    girls_count=name_frequency['F'])
                db.session.add(frequency_record)
                db.session.commit()

def read_name_frequencies():
    db.create_all()

    # Start with an empty list
    print("Deleting any previous data")
    db.session.query(NameFrequency).delete()
    db.session.query(Name).delete()
    db.session.commit()
    print("Done")

    names = {}

    # Get file list
    for filename in listdir('raw_data'):
        if filename[:3] == 'yob':
            read_frequencies_from_file(filename, names)

if __name__ == '__main__':
    read_name_frequencies()
