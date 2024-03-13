import requests
import json
import csv
import statistics
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
        issues(states: CLOSED) {
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
        repos.extend(response_data['data']['search']['nodes'])
        pageInfo = response_data['data']['search']['pageInfo']
        hasNextPage = pageInfo['hasNextPage']
        if not hasNextPage or len(repos) >= 1000:
            break
        cursor = pageInfo['endCursor']

    with open('./scripts/dataset/RQ06.csv', 'w', newline='') as csvfile:
        fieldnames = ['nameWithOwner', 'closedIssuesCount']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for repo in repos:
            writer.writerow({'nameWithOwner': repo['nameWithOwner'], 'closedIssuesCount': repo['issues']['totalCount'] if 'issues' in repo else 0})

    issues_counts = [repo['issues']['totalCount'] if 'issues' in repo else 0 for repo in repos]
    plt.hist(issues_counts, bins=20, edgecolor='black')
    plt.xlabel('Closed Issues Count')
    plt.ylabel('Number of Repositories')
    plt.title('Distribution of Closed Issues Count')
    plt.show()

    print("Média: ", statistics.mean(issues_counts))
    print("Moda: ", statistics.mode(issues_counts))
    print("Mediana: ", statistics.median(issues_counts))

get_all_repos()
