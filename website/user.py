import json
from . import db
from typing import Any
from .models import UserDB
from dataclasses import dataclass, field
from user_profile_details import github, codechef, codeforces

@dataclass
class User:
    flask_obj: Any
    friends: field(default_factory=tuple)

    upvotes: int = 0
    downvotes: int = 0

    github_username: str = ""
    codechef_username: str = ""
    codeforces_username: str = ""

    def __post_init__(self):
        if self.github_username:
            self.github_details = github.fetch_github_data(self.github_username)

        if self.codechef_username:
            self.codechef_details = codechef.fetch_codechef_data(self.codechef_username)

        if self.codeforces_username:
            self.codeforces_details = codeforces.fetch_codeforces_data(self.codeforces_username)


    def friend_leaderboard(self):
        leaderboard = []
        for friend_id in self.friends:
            friend = UserDB.query.filter_by(id=friend_id).first()
            leaderboard.append((friend.full_name, friend.email, friend.score))
        leaderboard.sort(key=lambda x: x[2], reverse=True)
        return leaderboard

    def update_rating(self):

        total_rating = self.upvotes + self.downvotes

        if self.codechef_rating:
            total_rating += (self.codechef_details['rating'] / 10)

        if self.codeforces_rating:
            total_rating += (self.codeforces_details['current rating'] / 10)

        if self.github_username:
            total_rating += self.github_details['total commits']
        
        try:
            self.flask_obj.score = total_rating
            db.session.commit()
        except Exception as e:
            print(e)
            
    def check_friend(self, friend_id):
        if friend_id in self.friends:
            return True
        return False
        
def get_user_obj(user):
    curr_user_json = dict()
    if user.is_authenticated:
        curr_user_json = json.loads(user.details)

    user_obj = User(
        flask_obj=user,
        
        upvotes=curr_user_json.get("upvotes", 0),
        downvotes=curr_user_json.get("downvotes", 0),
        friends=tuple(curr_user_json.get("friends", [])),

        github_username=curr_user_json.get("github_username", ""),
        codechef_username=curr_user_json.get("codechef_username", ""),
        codeforces_username=curr_user_json.get("codeforces_username", ""),
    )
    
    return user_obj