import json
from . import db
from .models import UserDB
from flask_login import current_user, login_required
from flask import Blueprint, redirect, request, flash, url_for

modify = Blueprint("modify", __name__)


@modify.route("/add_github", methods=["POST"])
@login_required
def add_github():
    username = request.form.get("github_username")
    try:
        curr_user_json = json.loads(current_user.details)
        curr_user_json["github_username"] = username
        curr_user_text = json.dumps(curr_user_json)

        current_user.details = curr_user_text
        db.session.commit()

    except Exception as e:
        print(f"\n\n{e}\n\n")
        flash("Unable to add Github", category="error")

    return redirect(url_for("views.refresh"))


@modify.route("/remove_github", methods=["POST"])
@login_required
def remove_github():
    try:
        curr_user_json = json.loads(current_user.details)
        curr_user_json["github_username"] = ""
        curr_user_text = json.dumps(curr_user_json)

        current_user.details = curr_user_text
        db.session.commit()

    except Exception as e:
        print(f"\n\n{e}\n\n")
        flash("Unable to remove Github", category="error")

    return redirect(url_for("views.refresh"))


@modify.route("/add_codeforces", methods=["POST"])
@login_required
def add_codeforces():
    username = request.form.get("codeforces_username")
    try:
        curr_user_json = json.loads(current_user.details)
        curr_user_json["codeforces_username"] = username
        curr_user_text = json.dumps(curr_user_json)

        current_user.details = curr_user_text
        db.session.commit()

    except Exception as e:
        print(f"\n\n{e}\n\n")
        flash("Unable to add CodeForces", category="error")

    return redirect(url_for("views.refresh"))


@modify.route("/remove_codeforces", methods=["POST"])
@login_required
def remove_codeforces():
    try:
        curr_user_json = json.loads(current_user.details)
        curr_user_json["codeforces_username"] = ""
        curr_user_text = json.dumps(curr_user_json)

        current_user.details = curr_user_text
        db.session.commit()

    except Exception as e:
        print(f"\n\n{e}\n\n")
        flash("Unable to remove CodeForces", category="error")

    return redirect(url_for("views.refresh"))


@modify.route("/add_codechef", methods=["POST"])
def add_codechef():
    username = request.form.get("codechef_username")
    try:
        curr_user_json = json.loads(current_user.details)
        curr_user_json["codechef_username"] = username
        curr_user_text = json.dumps(curr_user_json)

        current_user.details = curr_user_text
        db.session.commit()

    except Exception as e:
        print(f"\n\n{e}\n\n")
        flash("Unable to add Codechef", category="error")

    return redirect(url_for("views.refresh"))


@modify.route("/remove_codechef", methods=["POST"])
def remove_codechef():
    try:
        curr_user_json = json.loads(current_user.details)
        curr_user_json["codechef_username"] = ""
        curr_user_text = json.dumps(curr_user_json)

        current_user.details = curr_user_text
        db.session.commit()

    except Exception as e:
        print(f"\n\n{e}\n\n")
        flash("Unable to remove Codechef", category="error")

    return redirect(url_for("views.refresh"))


@modify.route("/add_friend", methods=["POST"])
@login_required
def add_friend():
    friend_id = request.form.get("friend_id")
    friend = UserDB.query.filter_by(id=friend_id).first()

    if not friend:
        flash("Friend not found", category="error")
        return redirect(url_for("views.refresh"))

    try:
        curr_user_json = json.loads(current_user.details)
        curr_user_json["friends"] = curr_user_json.get("friends", []) + [friend.id]
        curr_user_text = json.dumps(curr_user_json)

        current_user.details = curr_user_text
        db.session.commit()

    except Exception as e:
        print(f"\n\n{e}\n\n")
        flash("Unable to add friend", category="error")

    return redirect(url_for("views.refresh"))


@modify.route("/delete_friend", methods=["POST"])
@login_required
def delete_friend():
    friend_id = request.form.get("friend_id")
    friend = UserDB.query.filter_by(id=friend_id).first()

    try:
        curr_user_json = json.loads(current_user.details)
        curr_user_json["friends"].pop(curr_user_json["friends"].index(friend.id))
        curr_user_text = json.dumps(curr_user_json)

        current_user.details = curr_user_text
        db.session.commit()

    except Exception as e:
        print(f"\n\n{e}\n\n")
        flash("Unable to delete friend", category="error")

    return redirect(url_for("views.refresh"))


@modify.route("/upvote/<int:friend_id>", methods=["GET"])
@login_required
def add_upvote(friend_id):
    try:
        curr_user_json = json.loads(current_user.details)
        if friend_id in curr_user_json.get("upvotes", []):
            raise ValueError

        curr_user_json["upvotes"] = curr_user_json.get("upvotes", []) + [friend_id]
        curr_user_text = json.dumps(curr_user_json)

        current_user.details = curr_user_text
        db.session.commit()

    except Exception as e:
        print(f"\n\n{e}\n\n")
        flash("Unable to upvote user.", category="error")

    return redirect(url_for("views.refresh"))


@modify.route("/downvote/<int:friend_id>", methods=["GET"])
@login_required
def add_downvote(friend_id):
    try:
        curr_user_json = json.loads(current_user.details)
        if friend_id in curr_user_json.get("downvote", []):
            raise ValueError

        curr_user_json["downvote"] = curr_user_json.get("downvote", []) + [friend_id]
        curr_user_text = json.dumps(curr_user_json)

        current_user.details = curr_user_text
        db.session.commit()

    except Exception as e:
        print(f"\n\n{e}\n\n")
        flash("Unable to downvote user.", category="error")

    return redirect(url_for("views.refresh"))
