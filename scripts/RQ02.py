import requests
import json
import statistics
import csv
import matplotlib.pyplot as plt

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
        pullRequests(states: MERGED) {
          totalCount
        }
      }
    }
    pageInfo {
      endCursor
      hasNextPage
    }
  }
}
"""


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
                'pullRequests': node['pullRequests']['totalCount'] if 'pullRequests' in node else 0
            }
            repos.append(repository_info)
        pageInfo = response_data['data']['search']['pageInfo']
        hasNextPage = pageInfo['hasNextPage']
        if not hasNextPage or len(repos) >= 1000:
            break
        cursor = pageInfo['endCursor']


    with open('./scripts/dataset/RQ02.csv', 'w', newline='') as csvfile:
        fieldnames = ['nameWithOwner', 'pullRequests']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for repo in repos:
            writer.writerow(repo)


    pull_requests = [repo['pullRequests'] for repo in repos]
    plt.hist(pull_requests, bins=20, edgecolor='black')
    plt.xlabel('Number of Pull Requests')
    plt.ylabel('Number of Repositories')
    plt.title('Distribution of Pull Requests per Repository')
    plt.show()


    print("Média: ", statistics.mean(pull_requests))
    print("Moda: ", statistics.mode(pull_requests))
    print("Mediana: ", statistics.median(pull_requests))

get_all_repos()
