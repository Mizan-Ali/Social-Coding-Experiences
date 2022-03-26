import json
import requests

def main(username):
    url = f'https://api.github.com/users/{username}'
    response = requests.get(url).json()
    
    data_needed = ["company", "followers", "public_repos"]
    
    overall_data = {}
    for field in data_needed:
        overall_data[field] = response[field]
    overall_data.update(fetch_repos_data(username))
    return overall_data
    
    

def fetch_repos_data(username):
    page_no = 1
    repo_data = []
    repos_url = f'https://api.github.com/users/{username}/repos'
    
    while True:
        url = repos_url + '?page=' + str(page_no)
        response = requests.get(url).json()
        repos_fetched = len(response)
        repo_data.extend(response)
        if repos_fetched != 30:
            break
        page_no = page_no + 1
    
    data_needed = ["watchers_count", "forks_count", "stargazers_count"]
    data ={field: 0 for field in data_needed + ["commits_count"]}
    
    for repo in repo_data:
        for field in data_needed:
            data[field] += int(repo[field]) 
        # data["commits_count"] += fetch_commit_data(repo["git_commits_url"])
    return data
    
    
def fetch_commit_data(commits_url):
    page_no = 1
    commits = 0
    while (True):
        url = commits_url + '?page=' + str(page_no)
        response = requests.get(url).json()
        commits += len(response)
            
        if len(response) != 30:
            break
        page_no = page_no + 1
    return commits
            

if __name__ == "__main__":
    import time
    start = time.time()
    
    # print(main("Conero007"))
    # print(main("kb22"))
    
    end = time.time()
    print(end - start)