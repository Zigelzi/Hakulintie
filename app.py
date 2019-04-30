from flask import Flask, render_template, flash, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from os import environ
from datetime import datetime
from forms import Rekisteroidy, Kirjaudu

# Initializing the app and the DB.
app = Flask(__name__)
app.config['SECRET_KEY'] = environ['SECRET_KEY']
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)

# Creating the user and post table models
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(30), nullable=False)
    last_name = db.Column(db.String(30), nullable=False)
    house = db.Column(db.String(3), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    post = db.relationship('Post', backref='author', lazy=True)

    def __repr__(self):
        return f'User <{self.email} | {self.first_name} | {self.last_name} | {self.house}>'

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f'Post <{self.title} | {self.date_posted}>'

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
    if form.validate_on_submit():
        flash(f'Account created for {form.email.data}!', 'success')
        return redirect(url_for('index'))
    return render_template('rekisteroidy.html', title='Rekisteröidy', form=form)

@app.route("/kirjaudu", methods=["GET", "POST"])
def kirjaudu():
    form = Kirjaudu()
    return render_template('kirjaudu.html', title='Kirjaudu', form=form)

if __name__ == '__main__':
    app.run(debug=True)