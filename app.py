from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
app = Flask(__name__)

app.config['SECRET_KEY'] = '412ace50dc2f0e25f469ab1c9f457a02'

@app.route("/")
def index():
    return render_template('index.html', active='index')

@app.route("/vuosikello")
def vuosikello():
    return render_template('vuosikello.html', title='Vuosikello', active='vuosikello')

@app.route("/yhteystiedot")
def yhteystiedot():
    return render_template('yhteystiedot.html', title='Yhteystiedot', active='yhteystiedot')

@app.route("/kirjaudu")
def kirjaudu():
    return render_template('kirjaudu.html' title='Kirjaudu')

if __name__ == '__main__':
    app.run(debug=True)