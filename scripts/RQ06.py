import requests

with open("./token", "r") as token_file:
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

response = requests.post(url, json={'query': query}, headers=headers)
data = response.json()
print(data)
