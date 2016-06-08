from flask import Flask
from flask import render_template

app = Flask(__name__)
app.config['DEBUG'] = True

@app.route("/")
def hello():
    return render_template('helloworld.html')

if __name__ == "__main__":
    app.run()
