import json
from .user import User
from flask import Blueprint, render_template
from flask_login import login_required, current_user

views = Blueprint("views", __name__)


@views.route("/")
@login_required
def home():
    curr_user_json = json.loads(current_user.details)

    user_obj = User(
        flask_obj=current_user,
        
        upvotes=curr_user_json.get("upvotes", 0),
        downvotes=curr_user_json.get("downvotes", 0),
        friends=tuple(curr_user_json.get("friends", [])),

        github_username=curr_user_json.get("github_username", ""),
        codechef_username=curr_user_json.get("codechef_username", ""),
        codeforces_username=curr_user_json.get("codeforces_username", ""),
    )

    return render_template("profile.html", user=current_user, user_obj=user_obj)


