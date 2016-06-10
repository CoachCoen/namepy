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
