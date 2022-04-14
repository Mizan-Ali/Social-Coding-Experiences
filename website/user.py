from typing import List
from flask import flash
from logger import Logger
from flask_login import UserMixin
from .constants import user_constants
from dataclasses import dataclass, field
from .models import get_codechef, get_codeforces, get_github, mongo




@dataclass
class User(UserMixin):
    username: str
    email: str
    full_name: str
    password: str
    gender: str
    occupation: str = ""

    score: int = 0
    upvotes: int = 0
    downvotes: int = 0

    github_username: str = ""
    codechef_username: str = ""
    codeforces_username: str = ""

    friends: List[str] = field(default_factory=list)

    def get_id(self):
        return self.username

    @property
    def github_data(self):
        return get_github(self.github_username)

    @property
    def codechef_data(self):
        return get_codechef(self.codechef_username)

    @property
    def codeforces_data(self):
        return get_codeforces(self.codeforces_username)

    def check_friend(self, friend):
        if friend.username in self.friends:
            return True
        return False

    def is_upvoted(self, friend):
        votes_collection = mongo.db.votes
        vote = votes_collection.find_one(
            {
                "current_username": self.username,
                "friend_username": friend.username,
                "type": "upvote",
            }
        )
        if vote:
            return True
        return False

    def is_downvoted(self, friend):
        votes_collection = mongo.db.votes
        vote = votes_collection.find_one(
            {
                "current_username": self.username,
                "friend_username": friend.username,
                "type": "downvote",
            }
        )
        if vote:
            return True
        return False

    def update_rating(self):
        logger = Logger(mongo)
        function = 'update_rating'
        temp_score = 0

        if self.codechef_username:
            temp_score += 0.4 * int(self.codechef_data["rating"])
        if self.codeforces_username:
            temp_score += 0.4 * int(self.codeforces_data["rating"])
        if self.github_username:
            temp_score += 0.2 * int(self.github_data["total_commits"])

        self.score = round(temp_score + int(self.upvotes) - int(self.downvotes), 2)

        self.score = max(self.score, 0)
        logger.debug(3, function, f'Trying to update rating of user [{self.username}] to [{self.score}]')

        try:
            users_collection = mongo.db.users
            users_collection.update_one(
                {"_id": self.username}, {"$set": {"score": self.score}}, upsert=False
            )
            flash(3, user_constants["RATING_UPDATE_SUCCESS"], category="success")
            logger.debug(
                3,
                function_name=function,
                debug_message=user_constants["RATING_UPDATE_SUCCESS"],
                **self.__dict__
            )
        except Exception as e:
            flash(user_constants["RATING_UPDATE_FAILURE"], category="error")
            logger.error(
                3, function, user_constants["RATING_UPDATE_FAILURE"], **self.__dict__
            )


def get_user(username="", email=""):
    users_collection = mongo.db.users

    if username:
        user_data = users_collection.find_one({"_id": username})
    else:
        user_data = users_collection.find_one({"email": email})

    if user_data:
        return User(
            username=user_data["_id"],
            email=user_data["email"],
            full_name=user_data["full_name"],
            password=user_data["password"],
            gender=user_data["gender"],
            occupation=user_data.get("occupation", "None"),
            score=user_data.get("score", 0),
            upvotes=user_data.get("upvotes", 0),
            downvotes=user_data.get("downvotes", 0),
            github_username=user_data.get("github_username", ""),
            codechef_username=user_data.get("codechef_username", ""),
            codeforces_username=user_data.get("codeforces_username", ""),
            friends=user_data.get("friends", []),
        )


def save_user(username, email, full_name, password, gender, occupation):
    users_collection = mongo.db.users
    users_collection.insert_one(
        {
            "_id": username,
            "email": email,
            "full_name": full_name,
            "occupation": occupation,
            "gender": gender,
            "password": password,
        }
    )
