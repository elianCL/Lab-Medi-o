import requests
import json
from datetime import datetime

with open("./scripts/token", "r") as token_file:
    token = token_file.read().strip() 

url = 'https://api.github.com/graphql'
headers = {
    'Authorization': f'Bearer {token}',
}

query = """
query($cursor: String) {
  search(query: "stars:>0", type: REPOSITORY, first: 100, after: $cursor) {
    nodes {
      ... on Repository {
        nameWithOwner
        createdAt
      }
    }
    pageInfo {
      endCursor
      hasNextPage
    }
  }
}
"""
## Método que calcula a idade dos repositórios
def calculate_repository_age(creation_date):
    creation_datetime = datetime.strptime(creation_date, "%Y-%m-%dT%H:%M:%SZ")
    today = datetime.now()
    age = today.year - creation_datetime.year - ((today.month, today.day) < (creation_datetime.month, creation_datetime.day))
    return age

def get_repositories(cursor=None):
    response = requests.post(url, json={'query': query, 'variables': {'cursor': cursor}}, headers=headers)
    return response.json()

repos = []

def get_all_repos():
    cursor = None
    while True:
        response_data = get_repositories(cursor)
        for node in response_data['data']['search']['nodes']:
            repository_info = {
                'nameWithOwner': node['nameWithOwner'],
                'createdAt' : node['createdAt'],
                'age': calculate_repository_age(node['createdAt'])
            }
            repos.append(repository_info)
        pageInfo = response_data['data']['search']['pageInfo']
        hasNextPage = pageInfo['hasNextPage']
        if not hasNextPage or len(repos) >= 1000:
            break
        cursor = pageInfo['endCursor']

    with open('./scripts/dataset/RQ01.json', 'w') as file:
        json.dump(repos, file)
        
get_all_repos()
