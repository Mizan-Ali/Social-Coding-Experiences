from typing import Any
from dataclasses import dataclass
from user_profile_details import github, codechef, codeforces
from . import db

@dataclass(frozen=True)
class User:
    flask_obj: Any
    friends: tuple[int]

    score: int
    upvotes: int
    downvotes: int

    github_username: str
    codechef_username: str
    codeforces_username: str

    def __post_init__(self):
        if self.github_username:
            self.github_details = github.fetch_github_data(self.github_username)

        if self.codechef_username:
            self.codechef_details = codechef.fetch_codechef_data(self.codechef_username)

        if self.codeforces_username:
            self.codeforces_details = codeforces.fetch_codeforces_data(self.codeforces_username)


    def friend_leaderboard(self):
        pass

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
        
