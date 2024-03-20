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
        primaryLanguage {
          name
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

    with open('./scripts/dataset/RQ05.csv', 'w', newline='') as csvfile:
        fieldnames = ['nameWithOwner', 'primaryLanguage']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for repo in repos:
            writer.writerow({'nameWithOwner': repo['nameWithOwner'], 'primaryLanguage': repo['primaryLanguage']['name'] if repo['primaryLanguage'] else ''})

    languages = [repo['primaryLanguage']['name'] if repo['primaryLanguage'] else 'Unknown' for repo in repos]
    language_counts = {language: languages.count(language) for language in set(languages)}
    sorted_language_counts = dict(sorted(language_counts.items(), key=lambda item: item[1], reverse=True))
    plt.bar(sorted_language_counts.keys(), sorted_language_counts.values())
    plt.xlabel('Primary Language')
    plt.ylabel('Number of Repositories')
    plt.title('Distribution of Primary Languages')
    plt.xticks(rotation=45, ha='right')
    plt.show()

    counts = list(language_counts.values())
    print("Média: ", statistics.mean(counts))
    print("Moda: ", statistics.mode(counts))
    print("Mediana: ", statistics.median(counts))

get_all_repos()
