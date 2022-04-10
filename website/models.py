from flask import flash
from flask_pymongo import PyMongo
from user_profile_details import github, codechef, codeforces
from logger import Logger
from .constants import models_constants

mongo = PyMongo()
logger = Logger()


def get_github(username):
    github_collection = mongo.db.github
    github_data = github_collection.find_one({"_id": username})
    return github_data

def save_github(username):
    github_data = github.fetch_github_data(username)
    if github_data["SUCCESS"] is False:
        flash("Unable to save github data", category="error")
        raise ValueError("Unable to save github data")


    github_collection = mongo.db.github

    github_data["_id"] = github_data["username"]
    github_data.pop("username")
    github_data.pop("SUCCESS")

    github_collection.update_one({"_id": username}, {"$set": github_data}, upsert=True)


def get_codechef(username):
    codechef_collection = mongo.db.codechef
    codechef_data = codechef_collection.find_one({"_id": username})
    return codechef_data


def save_codechef(username):
    codechef_data = codechef.fetch_codechef_data(username)
    if codechef_data["SUCCESS"] is False:
        flash("Unable to save codechef data", category="error")
        raise ValueError("Unable to save codechef data")


    codechef_collection = mongo.db.codechef

    codechef_data["_id"] = codechef_data["username"]
    codechef_data.pop("username")
    codechef_data.pop("SUCCESS")

    codechef_collection.update_one({"_id": username}, {"$set": codechef_data}, upsert=True)


def get_codeforces(username):
    codeforces_collection = mongo.db.codeforces
    
    codeforces_data = codeforces_collection.find_one({"_id": username})
    return codeforces_data


def save_codeforces(username):
    codeforces_data = codeforces.fetch_codeforces_data(username)
    if codeforces_data["SUCCESS"] is False:
        flash("Unable to save codeforce data", category="error")
        raise ValueError("Unable to save codeforces data") 

    codeforces_collection = mongo.db.codeforces

    codeforces_data["_id"] = codeforces_data["username"]
    codeforces_data.pop("username")
    codeforces_data.pop("SUCCESS")

    codeforces_collection.update_one({"_id": username}, {"$set": codeforces_data}, upsert=True)

