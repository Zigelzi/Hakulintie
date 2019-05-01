from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Email, Length, EqualTo, ValidationError
from hakulintie.models import Users


# Form for registering new users.
class Rekisteroidy(FlaskForm):
    first_name = StringField('Etunimi', validators=[DataRequired()])
    last_name = StringField('Sukunimi', validators=[DataRequired()])
    house =  StringField('Asunto',
                         validators=[DataRequired(),
                                     Length(max=3, message='Talon numerossa voi olla vain kolme merkkikä')])
    email = StringField('Sähköposti',
                        validators=[DataRequired(), Email(message="Ei voimassa oleva sähköposti")])
    password = PasswordField('Salasana',
                             validators=[DataRequired(),
                                         Length(min=8, message="Salasanan täytyy olla vähintään 8 merkkiä pitkä")])
    confirm_pw = PasswordField('Vahvista salasana',
                               validators= [DataRequired(), EqualTo('password', message="Salasana ei täsmää")])
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
                        validators=[DataRequired(), Email(message="Ei voimassa oleva sähköposti")])
    password = PasswordField('Salasana',
                             validators=[DataRequired()])
    remember = BooleanField('Muista minut')
    submit = SubmitField('Kirjaudu sisään')