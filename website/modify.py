from . import db
from .views import update_rating
from flask_login import current_user, login_required
from user_profile_details import github, codechef, codeforces
from flask import Blueprint, redirect, request, flash, url_for
from .models import Codeforces, Friends, Github, User, Votes, Codechef

modify = Blueprint("modify", __name__)


@modify.route("/add_github", methods=["POST"])
@login_required
def add_github():
    username = request.form.get("github_username")
    current_user.github_username = username

    github_details = github.fetch_github_data(username)
    if not github_details["SUCCESS"]:
        flash("Unable to add Github", category="error")
        return redirect(url_for("views.home"))

    github_details.pop("SUCCESS")
    github_details.pop("company")
    github_details.pop("watchers_count")
    git = Github(user_id=current_user.id, **github_details)
    db.session.add(git)

    try:
        db.session.commit()
    except Exception as e:
        flash("Unable to add Github", category="error")

    update_rating()
    return redirect(url_for("views.home"))


@modify.route("/remove_github", methods=["POST"])
@login_required
def remove_github():
    try:
        current_user.github_username = ""
        git = Github.query.filter_by(user_id=current_user.id).first()
        db.session.delete(git)
        db.session.commit()
        flash("Removed Github", category="success")

    except Exception as e:
        flash("Unable to remove Github", category="error")

    update_rating()
    return redirect(url_for("views.home"))


@modify.route("/add_codeforces", methods=["POST"])
@login_required
def add_codeforces():
    username = request.form.get("codeforces_username")
    current_user.codeforces_username = username

    codeforces_details = codeforces.fetch_codeforces_data(username)

    if not codeforces_details["SUCCESS"]:
        flash("Unable to add Codeforces", category="error")
        raise redirect(url_for("views.home"))

    cf = Codeforces(
        user_id=current_user.id,
        rank = codeforces_details["rank"],
        rating =codeforces_details["rating"],
        problems_solved = codeforces_details["problems_solved"],
        contests = codeforces_details["contests"],
        highest_rating = codeforces_details["highest_rating"]
    )

    db.session.add(cf)
    try:
        db.session.commit()

    except Exception as e:
        flash("Unable to add Codeforces", category="error")
    
    update_rating()
    return redirect(url_for("views.home"))


@modify.route("/remove_codeforces", methods=["POST"])
@login_required
def remove_codeforces():
    try:
        current_user.codeforces_username = ""
        
        cf = Codeforces.query.filter_by(user_id=current_user.id).first()
        db.session.delete(cf)
        db.session.commit()
        flash("Codeforces added", category="success")

    except Exception as e:
        flash("Unable to remove CodeForces", category="error")

    update_rating()
    return redirect(url_for("views.home"))


@modify.route("/add_codechef", methods=["POST"])
def add_codechef():
    username = request.form.get("codechef_username")
    current_user.codechef_username = username

    try:
        db.session.commit()
    except Exception as e:
        flash("Unable to add Codechef", category="error")

    codechef_details = codechef.fetch_codechef_data(username)

    if not codechef_details["SUCCESS"]:
        raise ValueError

    codechef_details.pop("SUCCESS")
    cc = Codechef(
        user_id=current_user.id,
        rating=codechef_details["rating"],
        solved=codechef_details["solved"],
        country_rank=codechef_details["country_rank"],
        global_rank=codechef_details["global_rank"],
        highest_rating=codechef_details["highest_rating"],
        num_stars=codechef_details["num_stars"],
        country=codechef_details["country"],
    )

    db.session.add(cc)

    try:
        db.session.commit()
        update_rating()

    except Exception as e:
        flash("Unable to add Codechef", category="error")

    return redirect(url_for("views.home"))


@modify.route("/remove_codechef", methods=["POST"])
def remove_codechef():
    try:
        current_user.codechef_username = ""
        cc = current_user.codechef
        db.session.delete(cc)
        db.session.commit()

    except Exception as e:
        flash("Unable to remove Codechef", category="error")

    update_rating()
    return redirect(url_for("views.home"))


@modify.route("/add_friend", methods=["POST"])
@login_required
def add_friend():
    friend_id = request.form.get("friend_id")
    if current_user.id == int(friend_id):
        flash("Cannot follow self.", category="error")
        return redirect(url_for("views.home"))

    friend = User.query.filter_by(id=friend_id).first()

    if not friend:
        flash("User not found", category="error")
        return redirect(url_for("views.home"))

    try:
        new_friend = Friends(user_id=current_user.id, friend_id=friend_id)
        db.session.add(new_friend)
        db.session.commit()

    except Exception as e:
        flash("Unable to follow user", category="error")

    return redirect(url_for("views.home"))


@modify.route("/delete_friend", methods=["POST"])
@login_required
def delete_friend():
    friend_id = request.form.get("friend_id")
    friend_relaton = Friends.query.filter_by(
        user_id=current_user.id, friend_id=friend_id
    ).first()

    try:
        db.session.delete(friend_relaton)
        db.session.commit()

    except Exception as e:
        flash("Unable to unfollow user", category="error")

    return redirect(url_for("views.home"))


@modify.route("/upvote/<int:friend_id>")
@login_required
def add_upvote(friend_id):
    if current_user.id == friend_id:
        flash("Cannot upvote self", category="error")
        return redirect(url_for("views.home"))

    friend = User.query.get(friend_id)
    vote = Votes.query.filter_by(user_id=current_user.id, friend_id=friend_id).first()

    if vote:
        if vote.vote_type == "U":
            flash("Can only upvote once", category="error")
            return redirect(url_for("views.home"))
        else:
            db.session.delete(vote)
            friend.downvotes -= 1

    vote = Votes(user_id=current_user.id, friend_id=friend_id, vote_type="U")
    db.session.add(vote)
    friend.upvotes += 1

    try:
        db.session.commit()
        flash("Upvoted User", category="success")
    except Exception as e:
        flash("Unable to upvote user.", category="error")

    update_rating(friend)
    return redirect(url_for("views.home"))


@modify.route("/downvote/<int:friend_id>")
@login_required
def add_downvote(friend_id):
    if current_user.id == friend_id:
        flash("Cannot downvote self", category="error")
        return redirect(url_for("views.home"))

    friend = User.query.get(friend_id)
    vote = Votes.query.filter_by(user_id=current_user.id, friend_id=friend_id).first()

    if vote:
        if vote.vote_type == "D":
            flash("Can only downvote once", category="error")
            return redirect(url_for("views.home"))
        else:
            db.session.delete(vote)
            friend.upvotes -= 1

    vote = Votes(user_id=current_user.id, friend_id=friend_id, vote_type="D")
    db.session.add(vote)
    friend.downvotes += 1

    try:
        db.session.commit()
        flash("Downvoted User", category="success")
    except Exception as e:
        flash("Unable to downvote user.", category="error")

    update_rating(friend)
    return redirect(url_for("views.home"))
