from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect

app = Flask(__name__)
csrf = CSRFProtect(app)

# Move the database URI to a separate variable
db_uri = 'postgresql://postgres.ucxjsekrjjmujvckekuq:Juliet$$2006##@aws-0-us-west-1.pooler.supabase.com:5432/postgres'

# Set the database URI in the Flask app configuration
app.config["SQLALCHEMY_DATABASE_URI"] = db_uri
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True  # For automatically creating tables
app.config['SECRET_KEY'] = 'd9a1919dbf74170eb4f1d0d8'

# Initialize SQLAlchemy without attaching it to the app
db = SQLAlchemy(app)

# Import routes after initializing app
from cyberlink import routes
