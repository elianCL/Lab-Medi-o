import requests
import json
import csv
import matplotlib.pyplot as plt
from datetime import datetime
import statistics

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

    with open('./scripts/sprint-1/dataset/RQ01.csv', 'w', newline='') as csvfile:
        fieldnames = ['nameWithOwner', 'createdAt', 'age']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for repo in repos:
            writer.writerow(repo)

    ages = [repo['age'] for repo in repos]
    plt.hist(ages, bins=20, edgecolor='black')
    plt.xlabel('Idade dos repositórios')
    plt.ylabel('Número de repositórios')
    plt.title('Repositórios por idade')
    plt.show()


    print("Média: ", statistics.mean(ages))
    print("Moda: ", statistics.mode(ages))
    print("Mediana: ", statistics.median(ages))

get_all_repos()
