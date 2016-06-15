import string

import requests
from bs4 import BeautifulSoup

from app import db

from app.models import Set, LetterScore

def tidy_name(raw_name):
    # Only use first line
    result = raw_name.split('<')[0]

    # Remove anything past "(" or "#"
    result = result.split('(')[0].split('#')[0]

    # Remove 'letter', 'distribution' and 'Scrabble'
    for word in ['letter', 'distribution', 'Scrabble']:
        result = result.replace(word, '')

    return result.strip()

class PointsTable():
    def __init__(self, soup_table):
        # print(soup_table)
        self.name = tidy_name(soup_table.find('caption').text)
        self.soup_table = soup_table

    def parse_table(self):
        result = {}
        # First row contains the header - distribution, skip this
        for table_row in self.soup_table.findAll('tr')[1:]:
            row_value = int(table_row.find('th').text)
            for table_cell in table_row.findAll('td'):
                letters = table_cell.text.upper()
                letters = letters.replace('BLANK', '').replace(' ', '')
                for letter in letters:
                    if letter in string.uppercase:
                        result[letter] = row_value
        self.points = result

def extract_points(soup):
    languages_found = []
    result = []

    for soup_table in soup.findAll('table')[1:]:
        points_table = PointsTable(soup_table)

        # Only use first table for each language
        if not points_table.name in languages_found:
            points_table.parse_table()

            if points_table.points.keys():
                languages_found.append(points_table.name)
                result.append(points_table)

    return result

def store_points(points):
    for points_table in points:
        # Skip the 'Super' set, as it is not a separate language
        if points_table.name == 'Super':
            continue

        # Skip tables with an unprintable name
        try:
            print(points_table.name)
        except:
            continue


        set_record = Set(name=points_table.name)
        db.session.add(set_record)
        db.session.commit()

        for letter, score in points_table.points.iteritems():
            score_record = LetterScore(set_id=set_record.id, letter=letter, score=score)
            db.session.add(score_record)
            db.session.commit()

db.create_all()

print("Deleting any previous data")
db.session.query(LetterScore).delete()
db.session.query(Set).delete()
db.session.commit()
print("Done")

r = requests.get('https://en.wikipedia.org/wiki/Scrabble_letter_distributions')
soup = BeautifulSoup(r.text)

points = extract_points(soup)

store_points(points)
