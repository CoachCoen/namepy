from app import db

class Name(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String())
    frequencies = db.relationship('NameFrequency', backref='name', lazy='dynamic')

class NameFrequency(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name_id = db.Column(db.Integer, db.ForeignKey('name.id'))
    year = db.Column(db.Integer)
    boys_count = db.Column(db.Integer)
    girls_count = db.Column(db.Integer)

class Set(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String())
    scores = db.relationship('LetterScore', backref='set', lazy='dynamic')

class LetterScore(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    set_id = db.Column(db.Integer, db.ForeignKey('set.id'))
    score = db.Column(db.Integer)
    letter = db.Column(db.String(1))
