from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Email, Length, EqualTo


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
    

class Kirjaudu(FlaskForm):
    email = StringField('Sähköposti',
                            validators=[DataRequired(), Email(message="Ei voimassa oleva sähköposti")])
    password = PasswordField('Salasana',
                            validators=[DataRequired()])
    remember = BooleanField('Muista minut')
    submit = SubmitField('Kirjaudu sisään')