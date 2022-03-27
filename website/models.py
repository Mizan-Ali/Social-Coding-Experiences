from user_profile_details import github
from . import db
from flask_login import UserMixin


class Friends(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    friend_id = db.Column(db.Integer)


class Votes(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    friend_id = db.Column(db.Integer)
    vote_type = db.Column(db.String(1))


class Github(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    followers = db.Column(db.Integer)
    public_repos = db.Column(db.Integer)
    total_commits = db.Column(db.Integer)
    stargazers_count = db.Column(db.Integer)
    forks_count = db.Column(db.Integer)


class Codeforces(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    rank = db.Column(db.String(32))
    rating = db.Column(db.Integer)
    problems_solved = db.Column(db.Integer)
    contests = db.Column(db.Integer)
    highest_rating = db.Column(db.Integer)


class Codechef(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    rating = db.Column(db.Integer)
    solved = db.Column(db.Integer)
    country_rank = db.Column(db.Integer)
    global_rank = db.Column(db.Integer)
    highest_rating = db.Column(db.Integer)
    num_stars = db.Column(db.Integer)
    country = db.Column(db.String(32))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(64), unique=True)

    full_name = db.Column(db.String(64))
    password = db.Column(db.String(64))
    gender = db.Column(db.String(10))
    occupation = db.Column(db.String(64))

    upvotes = db.Column(db.Integer, default=0)
    downvotes = db.Column(db.Integer, default=0)
    score = db.Column(db.Integer, default=0)

    github_username = db.Column(db.String(64), default="")
    codechef_username = db.Column(db.String(64), default="")
    codeforces_username = db.Column(db.String(64), default="")

    friends = db.relationship("Friends")
    votes = db.relationship("Votes")
