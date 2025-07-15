from flask_login import UserMixin
from . import db

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    mobile = db.Column(db.String(30), unique=True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(1000))
    language = db.Column(db.String(2))
    theme = db.Column(db.String(5))
    admin = db.Column(db.Integer)
