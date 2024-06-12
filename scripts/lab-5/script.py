import requests
import time

def get_token():
    with open("./scripts/token", "r") as token_file:
        return token_file.read().strip()

rest_urls = [
    "https://api.github.com/repos/facebook/react",
    "https://api.github.com/repos/facebook/react/issues",
    "https://api.github.com/repos/facebook/react/contributors"
]

graphql_queries = [
    """
    {
      repository(owner: "facebook", name: "react") {
        name
        description
      }
    }
    """,
    """
    {
      repository(owner: "facebook", name: "react") {
        issues(first: 10) {
          edges {
            node {
              title
              body
            }
          }
        }
      }
    }
    """,
    """
    {
      repository(owner: "facebook", name: "react") {
        contributors(first: 10) {
          edges {
            node {
              login
            }
          }
        }
      }
    }
    """
]

graphql_url = "https://api.github.com/graphql"

headers = {
    "Authorization": f"Bearer {get_token()}",
    "Content-Type": "application/json"
}

def measure_rest(url):
    start_time = time.time()
    response = requests.get(url, headers=headers)
    end_time = time.time()
    duration = end_time - start_time
    size = len(response.content)
    return duration, size

def measure_graphql(query):
    start_time = time.time()
    response = requests.post(graphql_url, headers=headers, json={"query": query})
    end_time = time.time()
    duration = end_time - start_time
    size = len(response.content)
    return duration, size

def main():
    num_measurements = 10  # Número de medições

    rest_results = [[] for _ in range(len(rest_urls))]
    graphql_results = [[] for _ in range(len(graphql_queries))]

    for _ in range(num_measurements):
        for i, url in enumerate(rest_urls):
            rest_duration, rest_size = measure_rest(url)
            rest_results[i].append((rest_duration, rest_size))
        
        for i, query in enumerate(graphql_queries):
            graphql_duration, graphql_size = measure_graphql(query)
            graphql_results[i].append((graphql_duration, graphql_size))
    
    for i, results in enumerate(rest_results):
        durations = [result[0] for result in results]
        sizes = [result[1] for result in results]
        print(f"REST Query {i+1} - Tempo médio de resposta: {sum(durations) / len(durations)}")
        print(f"REST Query {i+1} - Tamanho médio da resposta: {sum(sizes) / len(sizes)}")

    for i, results in enumerate(graphql_results):
        durations = [result[0] for result in results]
        sizes = [result[1] for result in results]
        print(f"GraphQL Query {i+1} - Tempo médio de resposta: {sum(durations) / len(durations)}")
        print(f"GraphQL Query {i+1} - Tamanho médio da resposta: {sum(sizes) / len(sizes)}")

if __name__ == "__main__":
    main()
