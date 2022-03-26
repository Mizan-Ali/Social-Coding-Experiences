from email.policy import default
from . import db
from flask_login import UserMixin


class UserDB(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(64))
    email = db.Column(db.String(64), unique=True)
    password = db.Column(db.String(64))
    details = db.Column(db.String(256), default="{}")
    score = db.Column(db.Integer, default=0)
