from logger import Logger
from .user import get_user
from .constants import modify_constants
from flask_login import current_user, login_required
from flask import Blueprint, redirect, request, flash, url_for
from .models import mongo, save_codechef, save_codeforces, save_github

logger = Logger()
modify = Blueprint("modify", __name__)

@modify.route("/add_github", methods=["POST"])
@login_required
def add_github():
    function = 'modify.add_github'
    username = request.form.get("github_username")
    logger.debug(0, function, f'Attempting to add GitHub data for username [{username}] in DB')
    try:
        users_collections = mongo.db.users
        save_github(username)
        logger.debug(0, function, f'Adding GitHub username [{username}] DB for user [{current_user.username}]')
        users_collections.update_one({"_id": current_user.username}, {"$set": {"github_username": username}}, upsert=False)
        logger.debug(0, function, f'Added GitHub username [{username}] for user [{current_user.username}]')
        flash("Added Github", category="success")
        current_user.github_username = username
    except Exception as e:
        logger.error(0, function, f'Cannot add GitHub username [{username}] for user [{current_user.username}]. Error : [{e}]')
        flash("Unable to add Github", category="error")
    
    logger.debug(0, function, f'Updating the rating for user [{current_user.username}]')
    current_user.update_rating()
    return redirect(url_for("views.profile"))


@modify.route("/remove_github", methods=["POST"])
@login_required
def remove_github():
    function = 'modify.remove_github'
    try:
        logger.debug(0, function, f'Attempting to remove GitHub data for user [{current_user.username}]')
        users_collection = mongo.db.users
        users_collection.update_one({"_id" : current_user.username}, {"$set": {"github_username" : ""}}, upsert = False)
        github_collection = mongo.db.github
        github_collection.delete_one({"_id" : current_user.github_username})
        current_user.github_username = ""
        logger.debug(0, function, f'Removed GitHub data for user [{current_user.username}]')
        flash("Removed Github", category="success")

    except Exception as e:
        logger.error(0, function, f'Cannot remove GitHub data for user [{current_user.username}]. Error : [{e}]')
        flash("Unable to remove Github", category="error")

    logger.debug(0, function, f'Updating rating for user [{current_user.username}]')
    current_user.update_rating()
    return redirect(url_for("views.profile"))

@modify.route("/add_codeforces", methods=["POST"])
@login_required
def add_codeforces():
    function = 'modify.add_codeforces'
    username = request.form.get("codeforces_username")
    logger.debug(0, function, f'Adding CodeForces username [{username}] DB for user [{current_user.username}]')
    
    try:
        users_collections = mongo.db.users
        save_codeforces(username)
        users_collections.update_one({"_id": current_user.username}, {"$set": {"codeforces_username": username}}, upsert=False)
        current_user.codeforces = username
        logger.debug(0, function, f'Added CodeForces username [{username}] for user [{current_user.username}]')
    except Exception as e:
        logger.error(0, function, f'Cannot add CodeForces username [{username}] for user [{current_user.username}]. Error : [{e}]')
        flash("Unable to add Codeforces", category="error")

    logger.debug(0, function, f'Updating the rating for user [{current_user.username}]')
    current_user.update_rating()
    return redirect(url_for("views.profile"))


@modify.route("/remove_codeforces", methods=["POST"])
@login_required
def remove_codeforces():
    function = 'modify.remove_codeforces'
    try:
        logger.debug(0, function, f'Attempting to remove CodeForces data for user [{current_user.username}]')
        user_collections = mongo.db.users
        user_collections.update_one({"_id" : current_user.username}, {"$set": {"codeforces_username": ""}}, upsert=False)
        codeforces_collection = mongo.db.codeforces
        codeforces_collection.delete_one({"_id" : current_user.codeforces_username})
        current_user.codeforces_username = ""
        logger.debug(0, function, f'Removed CodeForces data for user [{current_user.username}]')
        flash("Codeforces added", category="success") 

    except Exception as e:
        flash("Unable to remove CodeForces", category="error")
        logger.error(0, function, f'Cannot remove CodeForces data for user [{current_user.username}]. Error : [{e}]')


    logger.debug(0, function, f'Updating rating for user [{current_user.username}]')
    current_user.update_rating()
    return redirect(url_for("views.profile"))


@modify.route("/add_codechef", methods=["POST"])
@login_required
def add_codechef():
    function = 'modify.add_codechef'
    username = request.form.get("codechef_username")
    logger.debug(0, function, f'Adding CodeChef username [{username}] DB for user [{current_user.username}]')
    
    try:
        users_collections = mongo.db.users
        save_codechef(username)
        users_collections.update_one({"_id": current_user.username}, {"$set": {"codechef_username": username}}, upsert=False)
        current_user.codechef_username = username
        logger.debug(0, function, f'Added CodeChef username [{username}] for user [{current_user.username}]')
    except Exception as e:
        logger.error(0, function, f'Cannot add CodeChef username [{username}] for user [{current_user.username}]. Error : [{e}]')
        flash("Unable to add Codechef", category="error")

    logger.debug(0, function, f'Updating the rating for user [{current_user.username}]')
    current_user.update_rating()
    return redirect(url_for("views.profile"))


@modify.route("/remove_codechef", methods=["POST"])
@login_required
def remove_codechef():
    function = 'modify.remove_codechef'

    try:
        logger.debug(0, function, f'Attempting to remove CodeChef data for user [{current_user.username}]')
        user_collections = mongo.db.users
        user_collections.update_one({"_id" : current_user.username}, {"$set": {"codechef_username": ""}}, upsert=False)
        codechef_collection = mongo.db.codechef
        codechef_collection.delete_one({"_id" : current_user.codechef_username})
        current_user.codechef_username = ""
        logger.debug(0, function, f'Removed CodeChef data for user [{current_user.username}]')
        flash("Removed Codechef", category = "success")

    except Exception as e:
        logger.error(0, function, f'Cannot remove CodeChef data for user [{current_user.username}]. Error : [{e}]')
        flash("Unable to remove Codechef", category="error")

    logger.debug(0, function, f'Updating the rating for user [{current_user.username}]')
    current_user.update_rating()
    return redirect(url_for("views.profile"))


@modify.route("/add_friend", methods=["POST"])
@login_required
def add_friend():
    function = 'modify.add_friend'
    friend_username = request.form.get("friend_username")
    logger.debug(0, function, f'[{current_user.username}] attempting to follow [{friend_username}]')
    if current_user.username == friend_username:
        logger.error(0, function, 'User is not allowed to follow self')
        flash("Cannot follow self.", category="error")
        return redirect(url_for("views.public_profile", username=friend_username))

    try:
        users_collection = mongo.db.users
        users_collection.update_one({"_id": current_user.username}, {"$push": {"friends": friend_username}}, upsert=False)
        logger.debug(0, function, f'Added user [{friend_username}] to friend list of user [{current_user.username}]')
        flash("Followed User", category="success")

    except Exception as e:
        logger.error(0, function, f'User [{current_user.username}] cannot follow user [{friend_username}]. Error : [{e}]')
        flash("Unable to follow user", category="error")

    return redirect(url_for("views.public_profile", username=friend_username))


@modify.route("/delete_friend", methods=["POST"])
@login_required
def delete_friend():
    function = 'modify.delete_friend'
    friend_username = request.form.get("friend_username")
    logger.debug(0, function, f'User [{current_user.username}] attempting to unfriend user [{friend_username}]')
    try:
        users_collection = mongo.db.users
        users_collection.update_one({"_id": current_user.username}, {"$pull": {"friends": friend_username}}, upsert=False)
        logger.debug(0, function, f'User [{current_user.username}] unfriended user [{friend_username}]')
        flash("Unfollowed User", category="success")
    except Exception as e:
        logger.error(0, function, f'User [{current_user.username}] cannot unfriend user [{friend_username}]. Error : [{e}]')
        flash("Unable to unfollow user", category="error")

    return redirect(url_for("views.public_profile", username=friend_username))


@modify.route("/upvote/<friend_username>")
@login_required
def add_upvote(friend_username):
    function = 'modify.add_upvote'
    logger.debug(3, function, f'User [{current_user.username}] attempting to upvote user [{friend_username}]')
    if current_user.username == friend_username:
        logger.error(0, function, f'User [{current_user.username}] cannot upvote self')
        flash("Cannot upvote self", category="error")
        return redirect(url_for("views.public_profile", username=friend_username))

    votes_collection = mongo.db.votes
    vote = votes_collection.find_one({"current_username": current_user.username, "friend_username": friend_username})
    is_voted = False
    if vote:
        is_voted = True
        if vote["type"] == "upvote":
            logger.debug(3, function, f'User [{current_user.username}] has already upvoted user [{friend_username}]. Removing upvote.')
            remove_upvote(friend_username)
            logger.debug(3, function, f'Removed upvote of user [{current_user.username}] successfully from user [{friend_username}]')
            return redirect(url_for("views.public_profile", username=friend_username))
    try:
        logger.debug(3, function, f'User [{current_user.username}] has not upvoted user [{friend_username}] yet. Adding upvote.')
        votes_collection.update_one({"current_username": current_user.username, "friend_username": friend_username}, {"$set": {"type": "upvote", "current_username": current_user.username, "friend_username": friend_username}}, upsert=True)

        users_collection = mongo.db.users

        users_collection.update_one({"_id": friend_username}, {"$inc": {"upvotes": 1, "downvotes": -1 if is_voted else 0}})

        friend = get_user(friend_username)
        friend.update_rating()
        logger.debug(3, function, f'Added upvote from user [{current_user.username}] to user [{friend_username}]')
        flash("Upvoted User", category="success")
    except Exception as e:
        logger.error(0, function, f'Failed add upvote from user [{current_user.username}] to user [{friend_username}]. Error : [{e}]')
        flash("Unable to upvote user.", category="error")

    return redirect(url_for("views.public_profile", username=friend_username))

def remove_upvote(friend_username):
    users_collection = mongo.db.users
    users_collection.update_one({"_id": friend_username}, {"$inc": {"upvotes": -1}}, upsert = False)

    votes_collection = mongo.db.votes
    votes_collection.delete_one({"current_username": current_user.username, "friend_username": friend_username})
    friend = get_user(friend_username)
    friend.update_rating()
    flash("Removed upvote", category="success")


@modify.route("/downvote/<friend_username>")
@login_required
def add_downvote(friend_username):
    function = 'modify.add_downvote'
    logger.debug(3, function, f'User [{current_user.username}] attempting to downvote user [{friend_username}]')

    if current_user.username == friend_username:
        logger.error(0, function, f'User [{current_user.username}] cannot downvote self')
        flash("Cannot downvote self", category="error")
        return redirect(url_for("views.public_profile", username=friend_username))

    votes_collection = mongo.db.votes
    vote = votes_collection.find_one({"current_username": current_user.username, "friend_username": friend_username})
    is_voted = False
    if vote:
        is_voted = True
        if vote["type"] == "downvote":
            logger.debug(3, function, f'User [{current_user.username}] has already downnvoted user [{friend_username}]. Removing downvote.')
            remove_downvote(friend_username)
            logger.debug(3, function, f'Removed downvote of user [{current_user.username}] successfully from user [{friend_username}]')
            return redirect(url_for("views.public_profile", username=friend_username))
    try:
        logger.debug(3, function, f'User [{current_user.username}] has not downvoted user [{friend_username}] yet. Adding downvote.')
        votes_collection.update_one({"current_username": current_user.username, "friend_username": friend_username}, {"$set": {"type": "downvote", "current_username": current_user.username, "friend_username": friend_username}}, upsert=True)

        users_collection = mongo.db.users
        users_collection.update_one({"_id": friend_username}, {"$inc": {"downvotes": 1, "upvotes": -1 if is_voted else 0}})

        friend = get_user(friend_username)
        friend.update_rating()

        flash("Downvoted User", category="success")
    except Exception as e:
        logger.error(0, function, f'Failed add downvote from user [{current_user.username}] to user [{friend_username}]. Error : [{e}]')
        flash("Unable to downvote user.", category="error")

    return redirect(url_for("views.public_profile", username=friend_username))

def remove_downvote(friend_username):
    users_collection = mongo.db.users
    users_collection.update_one({"_id": friend_username}, {"$inc": {"downvotes": -1}}, upsert = False)

    votes_collection = mongo.db.votes
    votes_collection.delete_one({"current_username": current_user.username, "friend_username": friend_username})
    friend = get_user(friend_username)
    friend.update_rating()
    flash("Removed downvote", category="success")