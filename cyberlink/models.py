from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from cyberlink import app, db
from enum import Enum  # provides options

# ==================== Defines a table Job for posting job opportunities =================================
class Job(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    title = db.Column(db.String(50), nullable=False)
    location = db.Column(db.String(50), nullable=False)
    salary = db.Column(db.Integer, nullable=False)
    currency = db.Column(db.String(10), nullable=False)
    image_address = db.Column(db.String(2000), nullable=False)
    responsibilities = db.Column(db.String(2000), nullable=True)
    requirements = db.Column(db.String(2000), nullable=True)


# ==================== Creating an enum for checking the user session ==============================
class UserSession(Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"


# ======================= Defines a table for storing site user data =======================================
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(length=30), nullable=False, unique=True)
    email_address = db.Column(db.String(length=50), nullable=False, unique=True)
    password_hash = db.Column(db.String(length=250), nullable=False)
    session_state = db.Column(db.Enum(UserSession), default=UserSession.INACTIVE, nullable=False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


# ====================== Defines a table for storing JOB applications ========================================
class Application(db.Model):
    app_id = db.Column(db.Integer, primary_key=True, nullable=False)
    title = db.Column(db.String(50), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    date_applied = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)


# ============================== Automatically create the database and the tables ======================================
with app.app_context():
    db.create_all()
