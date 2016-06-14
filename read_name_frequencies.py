# Runs both locally (using python index.py) and on WebFaction

# On WebFaction, must be run after activating the virtualenv

import random
import os
from os import listdir

from app import db

from app.models import Name, NameFrequency

def read_frequencies_from_file(filename, frequencies):
    year = int(filename[3:7])

    with open('raw_data/%s' % filename) as file:
        for line in file.readlines():
            try:
                name, sex, count = line.split(",")
            except:
                print("Couldn't parse line")
                print(line)
                print
                continue

            if name not in frequencies:
                frequencies[name] = {}

            if year not in frequencies[name]:
                frequencies[name][year] = {'F': 0, 'M': 0}

            frequencies[name][year][sex] = count

def dummy():

    name = Name.query.filter_by(name=name_text).first()

    if not name:
        name = Name(name=name_text)
        db.session.add(name)
        frequency = None
    else:
        frequency = NameFrequency.query.filter_by(name=name, year=year).first()

    if not frequency:
        frequency = NameFrequency(name=name, year=year)
        db.session.add(frequency)

    if sex == "F":
        frequency.boys_count = count
    elif sex == "M":
        frequency.girls_count = count
    else:
        print("Incorrect sex")
        print(line)
        print
        # continue

    db.session.commit()

def write_frequencies_to_database(frequencies):
    print("Writing frequencies to database")
    for name_text in frequencies.keys():
        name = Name(name=name_text)
        db.session.add(name)

        for year in frequencies[name_text].keys():
            frequency = NameFrequency(name=name, year=year, 
                            girls_count=frequencies[name_text][year]["F"],
                            boys_count=frequencies[name_text][year]["M"])
            db.session.add(frequency)
    db.session.commit()

def read_name_frequencies():
    # Start with an empty list
    db.session.query(NameFrequency).delete()
    db.session.query(Name).delete()
    db.session.commit()

    # To speed things up we'll read all names and frequencies in memory first
    result = {}

    # Get file list
    print("Reading frequencies from files")
    for filename in listdir('raw_data'):
        if filename[:3] == 'yob':
            read_frequencies_from_file(filename, result)

    write_frequencies_to_database(result)

def create_test_data():

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
    read_name_frequencies()
