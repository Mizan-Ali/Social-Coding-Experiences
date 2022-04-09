from unicodedata import category

from .user import User
from flask import flash
from flask_pymongo import PyMongo
from user_profile_details import github, codechef, codeforces


mongo = PyMongo()


def get_github(username):
    github_collection = mongo.db.github
    github_data = github_collection.find_one({"_id": username})
    return github_data

def save_github(username):
    github_data = github.fetch_github_data(username)
    if github_data["SUCCESS"] is False:
        flash("Unable to save github data", category="error")
        return 


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
        return 


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
        return 
        
    codeforces_collection = mongo.db.codeforces

    codeforces_data["_id"] = codeforces_data["username"]
    codeforces_data.pop("username")
    codeforces_data.pop("SUCCESS")

    codeforces_collection.update_one({"_id": username}, {"$set": codeforces_data}, upsert=True)


def get_user(username="", email=""):
    users_collection =  mongo.db.users
        
    if username:
        user_data = users_collection.find_one({"_id": username})
    else:
        user_data = users_collection.find_one({"email": email})


    if user_data:
        return User(
            username=username,
            email=user_data["email"],
            full_name=user_data["full_name"],
            password=user_data["password"],
            gender=user_data["gender"],
            occupation=user_data.get("occupation", "None"),

            score=user_data.get("score", 0),
            upvotes=user_data.get("upvotes", []),
            downvotes=user_data.get("downvotes", []),

            github_username=user_data.get("github_username", ""),
            codechef_username=user_data.get("codechef_username", ""),
            codeforces_username=user_data.get("codeforces_username", ""),

            friends=user_data.get("friends", []),
        )


def save_user(username, email, full_name, password, gender, occupation):
    users_collection = mongo.db.users
    users_collection.insert_one({
        "_id": username,
        "email": email,
        "full_name": full_name,
        "occupation": occupation,
        "gender": gender,
        "password": password
    })