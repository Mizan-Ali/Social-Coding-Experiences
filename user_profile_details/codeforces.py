import json
import requests
from bs4 import BeautifulSoup


def fetch_codeforces_data(username):
    response = requests.get(
        'https://codeforces.com/api/user.rating?handle=' + username)
    response_info = response.json()
    try:
        no_of_contests = len(response_info['result'])
        rating_response = requests.get('https://codeforces.com/api/user.info?handles=' + username)
        rating_info = rating_response.json()

        user_info = rating_info['result'][0]
        current_rating = user_info['rating']
        highest_rating = user_info['maxRating']
        rank = user_info['rank']
        problem_count = no_of_problems(username)
    except:
        return {'SUCCESS': False}

    return_dict = {
        "User Name": username,
        "Rank": rank,
        "Current Rating": current_rating,
        "Problems Solved": problem_count,
        "No of Contests": no_of_contests,
        "Highest Rating": highest_rating,
        "SUCCESS": True
    }
    return return_dict

def no_of_problems(username):
    resp = requests.get('http://codeforces.com/profile/' + username)
    soup = BeautifulSoup(resp.text, 'html.parser')
    problem_count = soup.find('div', class_ = '_UserActivityFrame_counterValue').text.split()[0]
    return problem_count
