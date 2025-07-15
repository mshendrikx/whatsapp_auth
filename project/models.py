from flask_login import UserMixin
from . import db

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True) # primary keys are required by SQLAlchemy
    admin = db.Column(db.Integer)
    name = db.Column(db.String(100))
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(1000))
    mobile = db.Column(db.String(30))
    language = db.Column(db.String(2))
    theme = db.Column(db.String(5))