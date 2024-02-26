from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin, LoginManager
from enum import Enum
from . import db, app

# Define LoginManager
login_manager = LoginManager()

# Define UserSession Enum for session state
class UserSession(Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"

# Define UserPermission Enum for user permissions
class UserPermission(Enum):
    ADMIN = "admin"
    USER = "user"

# Initialize LoginManager with the app
login_manager.init_app(app)

# Define User model
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(30), nullable=False, unique=True)
    email_address = db.Column(db.String(50), nullable=False, unique=True)
    password_hash = db.Column(db.String(250), nullable=False)
    session_state = db.Column(db.Enum(UserSession), default=UserSession.INACTIVE, nullable=False)
    user_permissions = db.Column(db.Enum(UserPermission), default=UserPermission.USER, nullable=False)
    registration_date = db.Column(db.TIMESTAMP, default=datetime.utcnow, nullable=False)
    sign_in_time = db.Column(db.TIMESTAMP)
    sign_out_time = db.Column(db.TIMESTAMP)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    # Required methods for Flask-Login
    def is_authenticated(self):
        return True

    def is_active(self):
        return self.session_state == UserSession.ACTIVE

    def is_anonymous(self):
        return False

    def get_id(self):
        return str(self.id)

# Define user loader function
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Define Job model
class Job(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    title = db.Column(db.String(50), nullable=False)
    location = db.Column(db.String(50), nullable=False)
    salary = db.Column(db.Integer, nullable=False)
    currency = db.Column(db.String(10), nullable=False)
    image_address = db.Column(db.String(2000), nullable=False)
    responsibilities = db.Column(db.String(2000), nullable=True)
    requirements = db.Column(db.String(2000), nullable=True)

# Define Application model
class Application(db.Model):
    app_id = db.Column(db.Integer, primary_key=True, nullable=False)
    title = db.Column(db.String(50), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    date_applied = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

# Automatically create the database and the tables
def create_tables():
    with app.app_context():
        db.create_all()

# Call create_tables function to create database tables
create_tables()

# Debug prints
print("Model.py loaded successfully.")
