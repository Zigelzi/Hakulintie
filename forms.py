from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Email, Length, EqualTo


class Rekisteroidy(FlaskForm):
    email = StringField('Sähköposti',
                            validators=[DataRequired(), Email()])
    password = PasswordField('Salasana',
                            validators=[DataRequired(),
                            Length(min=8, message="Salasanan täytyy olla vähintään 8 merkkiä pitkä.")])
    confirm_pw = PasswordField('Vahvista salasana',
                            validators= [DataRequired(), EqualTo('password')])
    submit = SubmitField('Luo tunnus')
    

class Kirjaudu(FlaskForm):
    email = StringField('Sähköposti',
                            validators=[DataRequired(), Email()])
    password = PasswordField('Salasana',
                            validators=[DataRequired()])
    remember = BooleanField('Muista minut')
    submit = SubmitField('Kirjaudu sisään')