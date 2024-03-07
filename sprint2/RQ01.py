import requests
import csv
from datetime import datetime


token = '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' 

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

def get_all_repos():
    cursor = None
    repos = []
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

    return repos

# Write repository data to CSV file
def write_to_csv(repos):
    with open('./scripts/dataset/RQ01.csv', 'w', newline='') as csvfile:
        fieldnames = ['nameWithOwner', 'age']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        for repo in repos:
            writer.writerow(repo)

# Main function
def main():
    repos = get_all_repos()
    write_to_csv(repos)

if __name__ == "__main__":
    main()
