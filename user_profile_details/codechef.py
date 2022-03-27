import requests


def fetch_codechef_data(username):
    try:
        response = requests.get(
            'https://codechef-userdetails-api.herokuapp.com/' + username)
        response_info = response.json()
        if 'error' in response_info:
            return {"SUCCESS": False}
        response_info["SUCCESS"] = True
        return response_info
    except:
        return {"SUCCESS": False}
