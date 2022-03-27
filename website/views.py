from .models import UserDB
from .user import get_user_obj
from flask import Blueprint, redirect, render_template, url_for
from flask_login import login_required, current_user

curr_user_obj = None
views = Blueprint("views", __name__)

@views.route("/")
@login_required
def home():
    if curr_user_obj is None:
        return redirect(url_for("views.refresh"))
    return render_template("profile.html", user_obj=curr_user_obj)

@views.route('/refresh')
@login_required
def refresh():
    global curr_user_obj
    curr_user_obj = get_user_obj(current_user)
    return redirect(url_for("views.home"))

@views.route("/leaderboard")
def global_leaderboard():
    leaderboard = []
    users = UserDB.query.all()
    
    for user in users:
        leaderboard.append((user.full_name, user.email, user.score))
    leaderboard.sort(key = lambda x: x[2], reverse=True)
    return leaderboard
  
@views.route("/public_profile/<string:email>")
@login_required
def public_profile(email):
    user = UserDB.query.filter_by(email=email).first()
    friend_user_obj = get_user_obj(user)
    
    return render_template("publicprofile.html", user_obj=curr_user_obj, friend_user_obj=friend_user_obj)
