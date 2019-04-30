from flask import render_template, flash, redirect, url_for
from hakulintie import app
from hakulintie.forms import Rekisteroidy, Kirjaudu


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
