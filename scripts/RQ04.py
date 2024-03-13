import requests
import json
import statistics
import csv
import matplotlib.pyplot as plt
from datetime import datetime
import pandas as pd

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
        updatedAt
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

    with open('./scripts/dataset/RQ04.csv', 'w', newline='') as csvfile:
        fieldnames = ['nameWithOwner', 'updatedAt']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for repo in repos:
            writer.writerow({'nameWithOwner': repo['nameWithOwner'], 'updatedAt': repo['updatedAt']})

    updated_dates = [datetime.strptime(repo['updatedAt'], "%Y-%m-%dT%H:%M:%SZ") for repo in repos]
    plt.hist(updated_dates, bins=20, edgecolor='black')
    plt.xlabel('Update Date')
    plt.ylabel('Number of Repositories')
    plt.title('Distribution of Update Dates')
    plt.show()


    df = pd.DataFrame(repos)
    df['updatedAt'] = pd.to_datetime(df['updatedAt'])
    deltas = df['updatedAt'] - df['updatedAt'].min()  
    mean_delta = df['updatedAt'].min() + pd.Timedelta(seconds=deltas.mean().total_seconds())  # Calculate mean
    mode_delta = df['updatedAt'].min() + deltas.mode().iloc[0]  
    median_delta = df['updatedAt'].min() + deltas.median()  

    print("Média: ", mean_delta)
    print("Moda: ", mode_delta)
    print("Mediana: ", median_delta)

get_all_repos()
