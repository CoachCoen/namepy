import random

from flask import Flask
from flask import render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://namepy_step4_user:step4@localhost/namepy_step4'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# from models import Name
from models import NameFrequency
# from models import Name, NameFrequency

@app.route("/")
def hello():
    return render_template('helloworld.html')
    # return render_template('helloworld.html', names=Name.query.all())

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

if __name__ == "__main__":
    app.run()
