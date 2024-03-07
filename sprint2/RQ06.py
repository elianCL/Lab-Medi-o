import requests
import csv

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

def get_all_repos():
    cursor = None
    repos = []
    while True:
        response_data = get_repositories(cursor)
        repos.extend(response_data['data']['search']['nodes'])
        pageInfo = response_data['data']['search']['pageInfo']
        hasNextPage = pageInfo['hasNextPage']
        if not hasNextPage or len(repos) >= 1000:
            break
        cursor = pageInfo['endCursor']

    return repos

# Write repository data to CSV file
def write_to_csv(repos):
    with open('./scripts/dataset/RQ06.csv', 'w', newline='') as csvfile:
        fieldnames = ['nameWithOwner', 'closedIssues']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        for repo in repos:
            closed_issues = repo['issues']['totalCount'] if 'issues' in repo else 0
            writer.writerow({
                'nameWithOwner': repo['nameWithOwner'],
                'closedIssues': closed_issues
            })

# Main function
def main():
    repos = get_all_repos()
    write_to_csv(repos)

if __name__ == "__main__":
    main()
