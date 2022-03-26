import requests


def fetch_codechef_data(username):
    try:
        response = requests.get(
            'https://codechef-userdetails-api.herokuapp.com/' + username)
        response_info = response.json()
        if 'error' in response_info:
            return {"SUCCESS": False}
        return response_info
    except:
        return {"SUCCESS": False}


if __name__ == "__main__":
    print(fetch_codechef_data("tourist"))
