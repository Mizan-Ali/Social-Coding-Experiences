from typing import List
from .models import get_codechef, get_codeforces, get_github, mongo
from flask_login import UserMixin
from dataclasses import dataclass, field

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

    # users_collection.find({"$or": [{"_id": "vafa"}, {"github_username": "vafa"}]"})

    friends = List[str] = field(default_factory=list)

    @property
    def github_data(self):
        return get_github(self.github_username)

    @property
    def codechef_data(self):
        return get_codechef(self.codechef_username)

    @property
    def codeforces_data(self):
        return get_codeforces(self.codeforces_username)

    def update_rating(self):
        # update in db as well
        pass