from flask import Flask,render_template, redirect, url_for, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect



app = Flask(__name__)
csrf = CSRFProtect(app)
db_uri = 'postgresql://postgres.ucxjsekrjjmujvckekuq:Juliet$$2006##@aws-0-us-west-1.pooler.supabase.com:5432/postgres'

# Set the database URI in the Flask app configuration
app.config["SQLALCHEMY_DATABASE_URI"] = db_uri
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True  # For automatically creating tables
app.config['SECRET_KEY']='d9a1919dbf74170eb4f1d0d8'
db = SQLAlchemy(app)
#Automatically Creating the database







































































































































































































































































































































































































































































































































































































































from cyberlink import routes