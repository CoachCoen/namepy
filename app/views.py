from flask import render_template
from app import app
from models import Name

@app.route("/")
def hello():
    return render_template('helloworld.html', names=Name.query.all())