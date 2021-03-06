from flask import render_template, flash, redirect, url_for, request, abort
from hakulintie import app, db, bcrypt
from hakulintie.forms import Rekisteroidy, Kirjaudu, PaivitaTili, LuoTiedote, MuokkaaTiedote
from hakulintie.models import Users, Posts
from flask_login import login_user, current_user, logout_user, login_required


@app.route("/")
def index():
    tiedotteet = Posts.query.order_by(Posts.date_posted.desc()).all()
    print(tiedotteet)
    return render_template('index.html', active='index', tiedotteet=tiedotteet)


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
        flash(f'Tunnuksesi on luotu, voit nyt kirjautua sisään.', 'success')
        return redirect(url_for('kirjaudu'))
    return render_template('rekisteroidy.html', title='Rekisteröidy', form=form, active='rekisteroidy')


@app.route("/kirjaudu", methods=["GET", "POST"])
def kirjaudu():
    # If current user exists, redirect to home.
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    form = Kirjaudu()

    # Validate the kirjaudu form input and if user exists log in.
    if form.validate_on_submit():
        user = Users.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            # Get the next page from URL when trying to access page which requires login but user isn't logged in
            next_page = request.args.get('next')
            # Redirect to next page parsed from URL if exist, if it doesn't exist then go to home page
            return redirect(next_page) if next_page else redirect(url_for('index'))
        else:
            # Login is failed and prompt the user for checking the email/password
            flash('Kirjautuminen epäonnistui. Tarkasta käyttäjänimi ja salasana.', 'alert')
    return render_template('kirjaudu.html', title='Kirjaudu', form=form, active='kirjaudu')


@app.route('/kirjaudu_ulos')
def kirjaudu_ulos():
    logout_user()
    return redirect(url_for('index'))


@app.route('/tili', methods=['GET', 'POST'])
# login_required decorator used to show that this page requires logged in user. Configuration in __init__.py
@login_required
def tili():
    form = PaivitaTili()
    if form.validate_on_submit():
        current_user.first_name = form.first_name.data
        current_user.last_name = form.last_name.data
        current_user.house = form.house.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Tiedot päivitetty!', 'success')
        return redirect(url_for('tili'))
    elif request.method == 'GET':
        form.first_name.data = current_user.first_name
        form.last_name.data = current_user.last_name
        form.house.data = current_user.house
        form.email.data = current_user.email
    return render_template('tili.html', title='Tilini', active='tili', form=form)

@app.route("/post/new", methods=['GET', 'POST'])
@login_required
def uusi_tiedote():
    form = LuoTiedote()
    if form.validate_on_submit():
        post = Posts(title=form.title.data, content=form.content.data, author=current_user)
        db.session.add(post)
        db.session.commit()
        flash('Tiedote luotu!', 'success')
        return redirect(url_for('index'))
    return render_template('create_post.html', title='Uusi tiedote', active='uusi_tiedote', form=form,
                           legend='Uusi tiedote')

@app.route("/tiedote/<int:tiedote_id>")
def tiedote(tiedote_id):
    tiedote = Posts.query.get_or_404(tiedote_id)
    return render_template('post.html', title=tiedote.title, tiedote=tiedote)


@app.route("/tiedote/<int:tiedote_id>/muokkaa", methods=['GET', 'POST'])
@login_required
def muokkaa_tiedotetta(tiedote_id):
    tiedote = Posts.query.get_or_404(tiedote_id)
    if tiedote.author != current_user:
        abort(403)
    form = MuokkaaTiedote()
    if form.validate_on_submit():
        tiedote.title = form.title.data
        tiedote.content = form.content.data
        db.session.commit()
        flash('Tiedote on päivitetty!', 'success')
        return redirect(url_for('tiedote', tiedote_id=tiedote.id))
    elif request.method == 'GET':
        form.title.data = tiedote.title
        form.content.data = tiedote.content
    return render_template('create_post.html', title='Muokkaa tiedotetta', tiedote=tiedote, form=form,
                           legend='Muokkaa tiedotetta')

@app.route("/tiedote/<int:tiedote_id>/poista", methods=['POST'])
@login_required
def poista_tiedote(tiedote_id):
    tiedote = Posts.query.get_or_404(tiedote_id)
    if tiedote.author != current_user:
        abort(403)
    db.session.delete(tiedote)
    db.session.commit()
    flash('Tiedote poistettu!', 'success')
    return redirect(url_for('index'))