from . import db
from flask_login import UserMixin

#1 upvote, downvote % based on givers ranking
#2 based participation in different platforms

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(64), unique=True)
    password = db.Column(db.String(64))
    full_name = db.Column(db.String(64))
    upvote = db.Column(db.Integer)
    downvote = db.Column(db.Integer)
    rating = db.Column(db.Integer)
    # friends = db.Columns(db.Array(db.Integer))