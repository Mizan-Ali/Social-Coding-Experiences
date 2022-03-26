from . import db
from flask_login import UserMixin


class UserDB(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(64), unique=True)

    full_name = db.Column(db.String(64))
    password = db.Column(db.String(64))
    
    score = db.Column(db.Integer, default=0)
    details = db.Column(db.String(256), default="{}")
    