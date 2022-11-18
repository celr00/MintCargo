import os
from flask import Flask, render_template
from flask_mysqldb import MySQL
from dotenv import load_dotenv

#Set .env variables into the os
load_dotenv()

app = Flask(__name__)

app.config['MYSQL_USER'] = os.environ['USER']
app.config['MYSQL_PASSWORD'] = os.environ['PASSWORD']
app.config['MYSQL_HOST'] = os.environ['HOST']
app.config['MYSQL_DB'] = os.environ['DB']

mysql = MySQL(app)

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/login')
def login():
    return render_template('login.html')


@app.route('/about')
def about():
    return render_template('about-us.html')


@app.route('/services')
def services():
    return render_template('services.html')


@app.route('/services/inland')
def inland():
    return render_template('inland.html')


@app.route('/services/air')
def air():
    return render_template('air.html')


@app.route('/services/maritime')
def maritime():
    return render_template('maritime.html')


@app.route('/services/storage')
def storage():
    return render_template('storage.html')


@app.route('/services/insurance')
def insurance():
    return render_template('insurance.html')


@app.route('/services/customs')
def customs():
    return render_template('customs.html')


@app.route('/services/representation')
def representation():
    return render_template('representation.html')


@app.route('/services/marketer')
def marketer():
    return render_template('marketer.html')


@app.route('/contact')
def contact():
    return render_template('contact.html')


@app.route('/privacy')
def privacy_policy():
    return render_template('privacy.html')

if __name__ == '__main__':
    app.run(debug=True)
