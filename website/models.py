from flask import flash
from logger import Logger
from flask_pymongo import PyMongo
from .constants import models_constants
from user_profile_details import github, codechef, codeforces

mongo = PyMongo()
logger = Logger()


def get_github(username):
    function = 'models.get_github'
    github_collection = mongo.db.github
    logger.debug(5, function, 'Attempting to get GitHub data from DB')
    github_data = github_collection.find_one({"_id": username})
    if github_data is not None:
        logger.debug(5, function, 'DB Response', **github_data)
    else:
        logger.error(0, function, f'GitHub data not in DB for user [{username}]')
    return github_data

def save_github(username):
    function = 'models.save_github'
    logger.debug(0, function, f'Attempting to fetch GitHub data for username [{username}]')
    github_data = github.fetch_github_data(username)
    if github_data["SUCCESS"] is False:
        logger.error(0, function, f'Unable to fetch GitHub data for [{username}]')
        flash("Unable to save GitHub data", category="error")
        raise ValueError("Unable to save GitHub data")

    logger.debug(0, function, f'GitHub data fetched for username [{username}]', **github_data)
    logger.debug(0, function, f'Saving GitHub data for username [{username}]')

    github_collection = mongo.db.github

    github_data["_id"] = github_data["username"]
    github_data.pop("username")
    github_data.pop("SUCCESS")

    github_collection.update_one({"_id": username}, {"$set": github_data}, upsert=True)
    logger.debug(0, function, f'GitHub data added successfully for username [{username}]')


def get_codechef(username):
    function = 'models.get_codechef'
    codechef_collection = mongo.db.codechef
    logger.debug(5, function, 'Attempting to get CodeChef data from DB')
    codechef_data = codechef_collection.find_one({"_id": username})
    if codechef_data is not None:
        logger.debug(5, function, 'DB Response', **codechef_data)
    else:
        logger.error(0, function, f'CodeChef data not in DB for user [{username}]')
    return codechef_data


def save_codechef(username):
    function = 'models.save_codechef'
    logger.debug(0, function, f'Attempting to fetch CodeChef data for username [{username}]')

    codechef_data = codechef.fetch_codechef_data(username)
    if codechef_data["SUCCESS"] is False:
        logger.error(0, function, f'Unable to fetch CodeChef data for [{username}]')
        flash("Unable to save codechef data", category="error")
        raise ValueError("Unable to save codechef data")

    logger.debug(0, function, f'CodeChef data fetched for username [{username}]', **codechef_data)
    logger.debug(0, function, f'Saving CodeChef data for username [{username}]')

    codechef_collection = mongo.db.codechef

    codechef_data["_id"] = codechef_data["username"]
    codechef_data.pop("username")
    codechef_data.pop("SUCCESS")

    codechef_collection.update_one({"_id": username}, {"$set": codechef_data}, upsert=True)
    logger.debug(0, function, f'CodeChef data added successfully for username [{username}]')


def get_codeforces(username):
    function = 'models.get_codeforces'
    codeforces_collection = mongo.db.codeforces
    logger.debug(5, function, 'Attempting to get CodeForces data from DB')
    codeforces_data = codeforces_collection.find_one({"_id": username})
    if codeforces_data is not None:
        logger.debug(5, function, 'DB Response', **codeforces_data)
    else:
        logger.error(0, function, f'CodeForces data not in DB for user [{username}]')
    return codeforces_data


def save_codeforces(username):
    function = 'models.save_codeforces'
    logger.debug(0, function, f'Attempting to fetch CodeForces data for username [{username}]')
    codeforces_data = codeforces.fetch_codeforces_data(username)
    if codeforces_data["SUCCESS"] is False:
        logger.error(0, function, f'Unable to fetch CodeForces data for [{username}]')
        flash("Unable to save codeforce data", category="error")
        raise ValueError("Unable to save codeforces data") 

    logger.debug(0, function, f'CodeForces data fetched for username [{username}]', **codeforces_data)
    logger.debug(0, function, f'Saving CodeForces data for username [{username}]')

    codeforces_collection = mongo.db.codeforces

    codeforces_data["_id"] = codeforces_data["username"]
    codeforces_data.pop("username")
    codeforces_data.pop("SUCCESS")

    codeforces_collection.update_one({"_id": username}, {"$set": codeforces_data}, upsert=True)
    logger.debug(0, function, f'CodeForces data added successfully for username [{username}]')
