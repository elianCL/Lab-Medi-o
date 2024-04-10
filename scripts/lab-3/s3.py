import csv
import requests

# Replace 'YOUR_ACCESS_TOKEN' with your personal access token
ACCESS_TOKEN = 'a'

def run_query(query, variables={}):
    url = 'https://api.github.com/graphql'
    headers = {'Authorization': f'bearer {ACCESS_TOKEN}'}
    request = requests.post(url, json={'query': query, 'variables': variables}, headers=headers)
    if request.status_code == 200:
        return request.json()
    else:
        raise Exception(f"Query falha {request.status_code}. {query}")

def get_top_repositories():
    total_repositories = []
    cursor = None
    while len(total_repositories) < 200:
        query = """
        query ($cursor: String) {
          search(query: "stars:>10000", type: REPOSITORY, first: 100, after: $cursor) {
            pageInfo {
              endCursor
              hasNextPage
            }
            nodes {
              ... on Repository {
                nameWithOwner
                pullRequests(first: 100) {
                  totalCount
                  nodes {
                    title
                    url
                    createdAt
                    closed
                    merged
                  }
                }
              }
            }
          }
        }
        """
        result = run_query(query, {'cursor': cursor})
        try:
            repositories = result['data']['search']['nodes']
            for repo in repositories:
                pr_count = repo['pullRequests']['totalCount']
                if pr_count >= 100:
                    total_repositories.append(repo)
            page_info = result['data']['search']['pageInfo']
            if page_info['hasNextPage']:
                cursor = page_info['endCursor']
            else:
                break
        except KeyError:
            print("Error: Failed to fetch data from GitHub API.")
            print("Response:", result)
            break
    return total_repositories

def save_to_csv(repositories):
    with open('pull_requests.csv', mode='w', newline='', encoding='utf-8') as file:
        fieldnames = ['Repository', 'Pull Request Title', 'URL', 'Created At', 'Closed', 'Merged']
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        for repo in repositories:
            for pr in repo['pullRequests']['nodes']:
                writer.writerow({
                    'Repository': repo['nameWithOwner'],
                    'Pull Request Title': pr['title'],
                    'URL': pr['url'],
                    'Created At': pr['createdAt'],
                    'Closed': pr['closed'],
                    'Merged': pr['merged']
                })

if __name__ == "__main__":
    repositories = get_top_repositories()
    if repositories:
        save_to_csv(repositories)
        print("Data saved to 'pull_requests.csv' successfully.")
    else:
        print("No repositories found or error occurred while fetching data.")
