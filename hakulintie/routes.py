from flask import render_template, flash, redirect, url_for
from hakulintie import app, db, bcrypt
from hakulintie.forms import Rekisteroidy, Kirjaudu
from hakulintie.models import Users, Posts
from flask_login import login_user, current_user


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

    # If current user exists, redirect to home.
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    form = Rekisteroidy()
    if form.validate_on_submit():
        # Hash the given PW to enter it to database
        hash_pw = bcrypt.generate_password_hash(form.password.data).decode('utf-8')

        # Take the form input and create db entry and commit it
        user = Users(first_name=form.first_name.data,
                     last_name=form.last_name.data,
                     house=form.house.data,
                     email=form.email.data,
                     password=hash_pw)
        db.session.add(user)
        db.session.commit()
        flash(f'Tunnuksesi on luotu, voit nyt kirjautua sisään.')
        return redirect(url_for('kirjaudu'))
    return render_template('rekisteroidy.html', title='Rekisteröidy', form=form)


@app.route("/kirjaudu", methods=["GET", "POST"])
def kirjaudu():
    # If current user exists, redirect to home.
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    form = Kirjaudu()

    if form.validate_on_submit():
        user = Users.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            return redirect(url_for('index'))
        else:
            flash('Kirjautuminen epäonnistui. Tarkasta käyttäjänimi ja salasana.')
    return render_template('kirjaudu.html', title='Kirjaudu', form=form)
