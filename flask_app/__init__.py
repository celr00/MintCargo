import os
from dotenv import load_dotenv
from flask import Flask
from flask_mysqldb import MySQL

# App creation
app = Flask(__name__)

# Set .env variables into the os
load_dotenv()

# Loading the os variables as app variables
app.config['MYSQL_USER'] = os.environ['USER']
app.config['MYSQL_PASSWORD'] = os.environ['PASSWORD']
app.config['MYSQL_HOST'] = os.environ['HOST']
app.config['MYSQL_DB'] = os.environ['DB']

# Connection to the database
mysql = MySQL(app)

# Secret Key for session purposes 
app.secret_key = '485o2'

# Routes made in other documents
from flask_app import public_routes, rewards_system, login
