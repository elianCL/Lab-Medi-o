import requests
import csv
import tqdm

with open("./scripts/token", "r") as token_file:
    token = token_file.read().strip()

url = 'https://api.github.com/graphql'
headers = {
    'Authorization': f'Bearer {token}',
}

query = """
query($cursor: String, $since: GitTimestamp!) {
  search(query: "language:java stars:>0", type: REPOSITORY, first: 100, after: $cursor) {
    nodes {
      ... on Repository {
        nameWithOwner
        createdAt
        stargazerCount
        defaultBranchRef {
          target {
            ... on Commit {
              history(since: $since) {
                totalCount
              }
            }
          }
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

def get_repositories(cursor=None, since="2023-01-01T00:00:00Z"):
    response = requests.post(url, json={'query': query, 'variables': {'cursor': cursor, 'since': since}}, headers=headers)
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
                'stargazerCount': node['stargazerCount'],
                'commitCount': node['defaultBranchRef']['target']['history']['totalCount']
            }
            repos.append(repository_info)
        pageInfo = response_data['data']['search']['pageInfo']
        hasNextPage = pageInfo['hasNextPage']
        if not hasNextPage or len(repos) >= 1000:
            break
        cursor = pageInfo['endCursor']

    return repos

def write_to_csv(repos):
    with open('./scripts/sprint-2/dataset/s2.csv', 'w', newline='') as csvfile:
        fieldnames = ['nameWithOwner', 'createdAt', 'stargazerCount', 'commitCount']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for repo in repos:
            writer.writerow(repo)

def main():
    repos = get_all_repos()
    write_to_csv(repos)

if __name__ == "__main__":
    main()
