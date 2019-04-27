from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from os import environ
from forms import Rekisteroidy, Kirjaudu
app = Flask(__name__)

app.config['SECRET_KEY'] = environ['SECRET_KEY']

@app.route("/")
def index():
    return render_template('index.html', active='index')

@app.route("/vuosikello")
def vuosikello():
    return render_template('vuosikello.html', title='Vuosikello', active='vuosikello')

@app.route("/yhteystiedot")
def yhteystiedot():
    return render_template('yhteystiedot.html', title='Yhteystiedot', active='yhteystiedot')

@app.route('/rekisteroidy', methods=["GET", "POST"])
def rekisteroidy():
    form = Rekisteroidy()
    return render_template('rekisteroidy.html', title='Rekisteröidy', form=form)

@app.route("/kirjaudu")
def kirjaudu():
    form = Kirjaudu()
    return render_template('kirjaudu.html', title='Kirjaudu', form=form)

if __name__ == '__main__':
    app.run(debug=True)