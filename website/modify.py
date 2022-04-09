from .user import get_user
from flask_login import current_user, login_required
from flask import Blueprint, redirect, request, flash, url_for
from .models import mongo, save_codechef, save_codeforces, save_github

modify = Blueprint("modify", __name__)

@modify.route("/add_github", methods=["POST"])
@login_required
def add_github():
    username = request.form.get("github_username")
    
    try:
        users_collections = mongo.db.users
        save_github(username)
        users_collections.update_one({"_id": current_user.username}, {"$set": {"github_username": username}}, upsert=False)
        flash("Added Github", category="success")
    except Exception as e:
        flash("Unable to add Github", category="error")

    current_user.update_rating()
    return redirect(url_for("views.home"))


@modify.route("/remove_github", methods=["POST"])
@login_required
def remove_github():
    try:
        users_collection = mongo.db.users
        users_collection.update_one({"_id" : current_user.username}, {"github_username" : ""}, upsert = False)
        github_collection = mongo.db.github
        github_collection.delete_one({"_id" : current_user.github_username})
        current_user.github_username = ""
        flash("Removed Github", category="success")

    except Exception as e:
        flash("Unable to remove Github", category="error")

    current_user.update_rating()
    return redirect(url_for("views.home"))


@modify.route("/add_codeforces", methods=["POST"])
@login_required
def add_codeforces():
    username = request.form.get("codeforces_username")
    
    try:
        users_collections = mongo.db.users
        save_codeforces(username)
        users_collections.update_one({"_id": current_user.username}, {"$set": {"codeforces_username": username}}, upsert=False)
    except Exception as e:
        flash("Unable to add Codeforces", category="error")

    current_user.update_rating()
    return redirect(url_for("views.home"))


@modify.route("/remove_codeforces", methods=["POST"])
@login_required
def remove_codeforces():
    try:
        user_collections = mongo.db.users
        user_collections.update_one({"_id" : current_user.username}, {"codeforces_username" : ""}, upsert=False)
        codeforces_collection = mongo.db.codeforces
        codeforces_collection.delete_one({"_id" : current_user.codeforces_username})
        current_user.codeforces_username = ""
        flash("Codeforces added", category="success") 

    except Exception as e:
        flash("Unable to remove CodeForces", category="error")

    current_user.update_rating()
    return redirect(url_for("views.home"))


@modify.route("/add_codechef", methods=["POST"])
def add_codechef():
    username = request.form.get("codechef_username")
    
    try:
        users_collections = mongo.db.users
        save_codechef(username)
        users_collections.update_one({"_id": current_user.username}, {"$set": {"codechef_username": username}}, upsert=False)
    except Exception as e:
        flash("Unable to add Codechef", category="error")

    current_user.update_rating()
    return redirect(url_for("views.home"))


@modify.route("/remove_codechef", methods=["POST"])
def remove_codechef():
    try:
        current_user.codechef_username = ""
        user_collections = mongo.db.user
        user_collections.update_one({"_id" : current_user.username}, {"codechef_username" : ""}, upsert=False)
        codechef_collection = mongo.db.codechef
        codechef_collection.delete_one({"_id" : current_user.codechef_username})
        current_user.codechef_username = ""      
        flash("Removed Codechef", category = "success")

    except Exception as e:
        flash("Unable to remove Codechef", category="error")

    current_user.update_rating()
    return redirect(url_for("views.home"))


@modify.route("/add_friend", methods=["POST"])
@login_required
def add_friend():
    friend_username = request.form.get("friend_username")
    if current_user.username == friend_username:
        flash("Cannot follow self.", category="error")
        return redirect(url_for("views.home"))

    try:
        users_collection = mongo.db.users
        users_collection.update_one({"_id": current_user.username}, {"$push": {"friends": friend_username}}, upsert=False)
        flash("Followed User", category="success")

    except Exception as e:
        flash("Unable to follow user", category="error")

    return redirect(url_for("views.home"))


@modify.route("/delete_friend", methods=["POST"])
@login_required
def delete_friend():
    friend_username = request.form.get("friend_username")
    try:
        users_collection = mongo.db.users
        users_collection.update_one({"_id": current_user.username}, {"$pull": {"friends": friend_username}}, upsert=False)

        flash("Unfollowed User", category="success")
    except Exception as e:
        flash("Unable to unfollow user", category="error")

    return redirect(url_for("views.home"))


@modify.route("/upvote/<friend_username>")
@login_required
def add_upvote(friend_username):
    if current_user.username == friend_username:
        flash("Cannot upvote self", category="error")
        return redirect(url_for("views.public_profile", username=friend_username))

    votes_collection = mongo.db.votes
    vote = votes_collection.find_one({"current_username": current_user.username, "friend_username": friend_username})
    is_voted = False
    if vote:
        is_voted = True
        if vote["type"] == "upvote":
            flash("Already upvoted", category="error")
            return redirect(url_for("views.public_profile", username=friend_username))
    try:
        votes_collection.update_one({"current_username": current_user.username, "friend_username": friend_username}, {"$set": {"type": "upvote", "current_username": current_user.username, "friend_username": friend_username}}, upsert=True)

        users_collection = mongo.db.users
        users_collection.update_one({"_id": friend_username}, {"$inc": {"upvote": 1, "downvote": -1 if is_voted else 0}})

        friend = get_user(friend_username)
        friend.update_rating()

        flash("Upvoted User", category="success")
    except Exception as e:
        flash("Unable to upvote user.", category="error")

    return redirect(url_for("views.public_profile", username=friend_username))


@modify.route("/downvote/<friend_username>")
@login_required
def add_downvote(friend_username):
    if current_user.username == friend_username:
        flash("Cannot downvote self", category="error")
        return redirect(url_for("views.public_profile", username=friend_username))

    votes_collection = mongo.db.votes
    vote = votes_collection.find_one({"current_username": current_user.username, "friend_username": friend_username})
    is_voted = False
    if vote:
        is_voted = True
        if vote["type"] == "downvote":
            flash("Already downvoted", category="error")
            return redirect(url_for("views.public_profile", username=friend_username))
    try:
        votes_collection.update_one({"current_username": current_user.username, "friend_username": friend_username}, {"$set": {"type": "downvote", "current_username": current_user.username, "friend_username": friend_username}}, upsert=True)

        users_collection = mongo.db.users
        users_collection.update_one({"_id": friend_username}, {"$inc": {"downvote": 1, "upvote": -1 if is_voted else 0}})

        friend = get_user(friend_username)
        friend.update_rating()

        flash("Downvoted User", category="success")
    except Exception as e:
        flash("Unable to downvote user.", category="error")

    return redirect(url_for("views.public_profile", username=friend_username))
