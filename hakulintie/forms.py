from flask_wtf import FlaskForm
from flask_login import current_user
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField
from wtforms.validators import DataRequired, Email, Length, EqualTo, ValidationError
from hakulintie.models import Users

data_req_msg = 'Pakollinen kenttä'

# Form for registering new users.
class Rekisteroidy(FlaskForm):
    first_name = StringField('Etunimi', validators=[DataRequired(message=data_req_msg)])
    last_name = StringField('Sukunimi', validators=[DataRequired(message=data_req_msg)])
    house =  StringField('Asunto',
                         validators=[DataRequired(message=data_req_msg),
                                     Length(max=3, message='Talon numerossa voi olla vain kolme merkkikä')])
    email = StringField('Sähköposti',
                        validators=[DataRequired(message=data_req_msg), Email(message="Ei voimassa oleva sähköposti")])
    password = PasswordField('Salasana',
                             validators=[DataRequired(message=data_req_msg),
                                         Length(min=8, message="Salasanan täytyy olla vähintään 8 merkkiä pitkä")])
    confirm_pw = PasswordField('Vahvista salasana',
                               validators= [DataRequired(message=data_req_msg), EqualTo('password', message="Salasana ei täsmää")])
    submit = SubmitField('Luo tunnus')

    # Custom validation to validate that email is not in use
    def validate_email(self, email):

        # Get the email from the form and query the DB for it
        email = Users.query.filter_by(email=email.data).first()

        # If the DB query returns something, raise validation error
        if email:
            raise ValidationError('Tämä sähköpostiosoite on jo käytössä.')


# Form for logging in to the site.
class Kirjaudu(FlaskForm):
    email = StringField('Sähköposti',
                        validators=[DataRequired(message=data_req_msg), Email(message="Ei voimassa oleva sähköposti")])
    password = PasswordField('Salasana',
                             validators=[DataRequired(message=data_req_msg)])
    remember = BooleanField('Muista minut')
    submit = SubmitField('Kirjaudu sisään')

# Form for registering new users.
class PaivitaTili(FlaskForm):
    first_name = StringField('Etunimi', validators=[DataRequired(message=data_req_msg)])
    last_name = StringField('Sukunimi', validators=[DataRequired(message=data_req_msg)])
    house =  StringField('Asunto',
                         validators=[DataRequired(message=data_req_msg),
                                     Length(max=3, message='Talon numerossa voi olla vain kolme merkkikä')])
    email = StringField('Sähköposti',
                        validators=[DataRequired(message=data_req_msg), Email(message="Ei voimassa oleva sähköposti")])
    submit = SubmitField('Päivitä tiedot')

    # Custom validation to validate that email is not in use
    def validate_email(self, email):

        if email.data != current_user.email:
            # Get the email from the form and query the DB for it
            email = Users.query.filter_by(email=email.data).first()
            # If the DB query returns something, raise validation error
            if email:
                raise ValidationError('Tämä sähköpostiosoite on jo käytössä.')

class LuoTiedote(FlaskForm):
    title = StringField('Tiedotteen otsikko', validators=[DataRequired(message=data_req_msg)])
    content = TextAreaField('Tiedotteen sisältö', validators=[DataRequired(message=data_req_msg)])
    submit = SubmitField('Luo tiedote')

class MuokkaaTiedote(FlaskForm):
    title = StringField('Tiedotteen otsikko', validators=[DataRequired(message=data_req_msg)])
    content = TextAreaField('Tiedotteen sisältö', validators=[DataRequired(message=data_req_msg)])
    submit = SubmitField('Muokkaa tiedotetta')
