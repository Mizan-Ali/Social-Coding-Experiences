from typing import List
from flask_login import UserMixin
from dataclasses import dataclass, field
from .models import get_codechef, get_codeforces, get_github, mongo
from logger import Logger
from .constants import user_constants

logger = Logger()

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

    # users_collection.find({"$or": [{"_id": "vafa"}, {"github_username": "vafa"}]"})

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

    def update_rating(self):
        ac_count = 0
        temp_score = 0

        if self.codechef_username:
            temp_score += 0.4 * int(self.codechef_data['rating'])
            ac_count += 1
        if self.codeforces_username:
            temp_score += 0.4 * int(self.codeforces_data['rating'])
            ac_count += 1
        if self.github_username:
            temp_score += 0.2 * int(self.github_data['total_commits'])
            ac_count += 1

        self.score = round((temp_score / float(ac_count)) + int(self.upvotes) - int(self.downvotes), 2)

        if self.score < 0:
            self.score = 0
        
        users_collection = mongo.db.users
        users_collection.update_one({'_id' : self.username}, {'$set' : {'score': self.score}}, upsert = False)


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
    users_collection.insert_one({
        "_id": username,
        "email": email,
        "full_name": full_name,
        "occupation": occupation,
        "gender": gender,
        "password": password
    })
