from . import db
from flask_login import login_required, current_user
from user_profile_details import github, codechef, codeforces
from .models import Codechef, Codeforces, Friends, Github, User
from flask import Blueprint, flash, redirect, render_template, request, url_for


views = Blueprint("views", __name__)


@views.route("/")
@login_required
def home():
    git = Github.query.filter_by(user_id=current_user.id).first()
    cf = Codeforces.query.filter_by(user_id=current_user.id).first()
    cc = Codechef.query.filter_by(user_id=current_user.id).first()
    return render_template(
        "profile.html", user=current_user, github=git, codechef=cc, codeforces=cf
    )


@views.route("/public_profile", methods=["POST"])
@login_required
def public_profile():
    email = request.form.get("email", "")
    if not email:
        return redirect(url_for("view.home"))

    friend = User.query.filter_by(email=email).first()
    if not friend:
        flash("User does not exist.", category="error")
        return redirect((url_for("views.home")))

    isfriend = bool(
        Friends.query.filter_by(user_id=current_user.id, friend_id=friend.id).first()
    )

    git = Github.query.filter_by(user_id=friend.id).first()
    cf = Codeforces.query.filter_by(user_id=friend.id).first()
    cc = Codechef.query.filter_by(user_id=friend.id).first()

    return render_template(
        "publicprofile.html",
        user=current_user,
        friend=friend,
        isfriend=isfriend,
        github=git,
        codechef=cc,
        codeforces=cf,
    )


@views.route("/leaderboard")
def leaderboard():
    global_leaderboard = get_global_leaderboard()
    friends_leaderboard = get_friend_leaderboard()

    return render_template(
        "leaderboard.html",
        user=current_user,
        global_leaderboard=global_leaderboard,
        friends_leaderboard=friends_leaderboard,
    )


@views.route("/refresh_github", methods=["POST"])
@login_required
def refresh_github():
    git = Github.query.filter_by(user_id=current_user.id)
    github_details = github.fetch_github_data(current_user.github_username)

    git.update(
        {
            "followers": github_details["followers"],
            "public_repos": github_details["public_repos"],
            "total_commits": github_details["total_commits"],
            "stargazers_count": github_details["stargazers_count"],
            "forks_count": github_details["forks_count"],
        }
    )

    try:
        db.session.commit()
        flash("Updated GitHub", category="success")
    except Exception as e:
        flash("Unable to add Github", category="error")

    update_rating()
    return redirect(url_for("views.home"))


@views.route("/refresh_codeforces", methods=["POST"])
@login_required
def refresh_codeforces():
    cf = Codeforces.query.filter_by(user_id=current_user.id)
    codeforces_details = codeforces.fetch_codeforces_data(
        current_user.codeforces_username
    )

    cf.update(
        {
            "rank": codeforces_details["rank"],
            "rating": codeforces_details["rating"],
            "problems_solved": codeforces_details["problems_solved"],
            "contests": codeforces_details["contests"],
            "highest_rating": codeforces_details["highest_rating"],
        }
    )

    try:
        db.session.commit()
        flash("Updated Codeforces", category="success")
    except Exception as e:
        flash("Unable to add Codeforces", category="error")

    update_rating()
    return redirect(url_for("views.home"))


@views.route("/refresh_codechef", methods=["POST"])
@login_required
def refresh_codechef():
    cc = Codechef.query.filter_by(user_id=current_user.id)
    codechef_details = codechef.fetch_codechef_data(current_user.codechef_username)

    cc.update(
        {
            "rating": codechef_details["rating"],
            "solved": codechef_details["solved"],
            "country_rank": codechef_details["country_rank"],
            "global_rank": codechef_details["global_rank"],
            "highest_rating": codechef_details["highest_rating"],
            "num_stars": codechef_details["num_stars"],
            "country": codechef_details["country"],
        }
    )

    try:
        db.session.commit()
        flash("Updated Codechef", category="success")
    except Exception as e:
        flash("Unable to add Codechef", category="error")

    update_rating()
    return redirect(url_for("views.home"))


def get_global_leaderboard():
    leaderboard = []
    for user in User.query.all():
        leaderboard.append((user.full_name, user.email, user.score))
    leaderboard.sort(key=lambda x: x[2], reverse=True)
    return leaderboard


def get_friend_leaderboard():
    leaderboard = [(current_user.full_name, current_user.email, current_user.score)]
    for friend_relation in current_user.friends:
        friend = User.query.get(friend_relation.friend_id)
        leaderboard.append((friend.full_name, friend.email, friend.score))
    leaderboard.sort(key=lambda x: x[2], reverse=True)
    return leaderboard


def update_rating(user=current_user):
    total_rating = user.upvotes - user.downvotes

    if current_user.codechef_username:
        cc = Codechef.query.filter_by(user_id=user.id).first()
        total_rating += cc.rating / 10

    if current_user.codeforces_username:
        cf = Codeforces.query.filter_by(user_id=user.id).first()
        total_rating += cf.rating / 10

    if current_user.github_username:
        git = Github.query.filter_by(user_id=user.id).first()
        total_rating += git.total_commits

    try:
        user.score = total_rating
        db.session.commit()

        flash("Updated rating", category="success")
    except Exception as e:
        flash("Could not update rating", category="error")
