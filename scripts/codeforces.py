import json
import requests

def fetch(username):
    response = requests.get('https://codeforces.com/api/user.rating?handle=' + username)
    response_info = response.json()

    try:
        current_rating = response_info['result'][-1]['newRating']
        no_of_contests = len(response_info['result'])
        highest_rating = max([contest['newRating'] for contest in response_info['result']])
    except:
        return {'SUCCESS': False}

    return_dict =  {
        "User Name": username,
        "Current Rating": current_rating,
        "No of Contests": no_of_contests,
        "Highest Rating": highest_rating,
        "SUCCESS": True
    }
    
    return return_dict

if __name__ == "__main__":
    print(fetch("tourist"))