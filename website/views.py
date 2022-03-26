import json
from . import db
from .user import User
from .models import UserDB
from flask_login import login_required, current_user
from flask import Blueprint, redirect, render_template, request, flash, url_for

views = Blueprint("views", __name__)


@views.route("/")
def home():
    curr_user_json = json.load(current_user.details)

    user_obj = User(
        flask_obj=current_user,
        
        upvotes=curr_user_json.get("upvotes", 0),
        downvotes=curr_user_json.get("downvotes", 0),
        friends=tuple(curr_user_json.get("friends", [])),

        github_username=curr_user_json.get("github_username", ""),
        codechef_username=curr_user_json.get("codechef_username", ""),
        codeforces_username=curr_user_json.get("codeforces_username", ""),
    )

    return render_template("home.html", user=user_obj)


@views.route("/add_friend", METHOD=["POST"])
def add_friend():
    friend_email = request.form.get("friendEmail")
    friend = UserDB.query.filter_by(email=friend_email).first()

    if not friend:
        flash("Friend not found", category="error")
        return redirect(url_for("views.home"))

    try:
        curr_user_json = json.load(current_user.details)
        curr_user_json["friends"] = curr_user_json.get("friends", []) + [friend.id]
        curr_user_text = json.dumps(curr_user_json)

        current_user.details = curr_user_text
        db.session.commit()

    except Exception as e:
        print(f"\n\n{e}\n\n")
        flash("Unable to add friend", category="error")

    return redirect(url_for("views.home"))


@views.route("/delete_friend", METHOD=["POST"])
def delete_friend():
    friend_email = request.form.get("friendEmail")
    friend = UserDB.query.filter_by(email=friend_email).first()

    try:
        curr_user_json = json.load(current_user.details)
        curr_user_json["friends"].pop(curr_user_json["friends"].index(friend.id))
        curr_user_text = json.dumps(curr_user_json)

        current_user.details = curr_user_text
        db.session.commit()

    except Exception as e:
        print(f"\n\n{e}\n\n")
        flash("Unable to delete friend", category="error")

    return redirect(url_for("views.home"))
