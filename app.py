from flask import Flask, render_template
app = Flask(__name__)

@app.route("/")
def index():
    return render_template('index.html')

@app.route("/vuosikello")
def vuosikello():
    return render_template('vuosikello.html')

@app.route("/yhteystiedot")
def yhteystiedot():
    return render_template('yhteystiedot.html')

if __name__ == '__main__':
    app.run(debug=True)