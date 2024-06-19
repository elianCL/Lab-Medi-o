import requests
import time
import csv
import matplotlib.pyplot as plt
from tqdm import tqdm

def get_token():
    with open("./scripts/token", "r") as token_file:
        return token_file.read().strip()

rest_urls = {
    "user_repos": "https://api.github.com/users/octocat/repos",
    "repo_info": "https://api.github.com/repos/octocat/Hello-World",
    "top_repos": "https://api.github.com/search/repositories?q=stars:>1&sort=stars&order=desc&per_page=10"
}

graphql_queries = {
    "user_repos": '''
    {
      user(login: "octocat") {
        repositories(first: 100) {
          nodes {
            name
            url
          }
        }
      }
    }
    ''',
    "repo_info": '''
    {
      repository(owner: "octocat", name: "Hello-World") {
        name
        description
        url
      }
    }
    ''',
    "top_repos": '''
    {
      search(query: "stars:>1", type: REPOSITORY, first: 10) {
        edges {
          node {
            ... on Repository {
              name
              url
              stargazerCount
            }
          }
        }
      }
    }
    '''
}

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

def run_tests(num_measurements):
    rest_results = {key: [] for key in rest_urls}
    graphql_results = {key: [] for key in graphql_queries}

    with tqdm(total=num_measurements * (len(rest_urls) + len(graphql_queries))) as pbar:
        for _ in range(num_measurements):
            for key, url in rest_urls.items():
                rest_duration, rest_size = measure_rest(url)
                rest_results[key].append((rest_duration, rest_size))
                pbar.update(1)
            
            for key in graphql_queries:
                graphql_duration, graphql_size = measure_graphql(graphql_queries[key])
                graphql_results[key].append((graphql_duration, graphql_size))
                pbar.update(1)
    
    with open('./scripts/lab-5/api_comparison_results.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['API Type', 'Query Type', 'Response Time', 'Response Size'])
        for key, results in rest_results.items():
            for duration, size in results:
                writer.writerow(['REST', key, duration, size])
        for key, results in graphql_results.items():
            for duration, size in results:
                writer.writerow(['GraphQL', key, duration, size])
    
    return rest_results, graphql_results

def analyze_results(rest_results, graphql_results):
    response_sizes = []
    
    for key in rest_results:
        rest_durations = [result[0] for result in rest_results[key]]
        graphql_durations = [result[0] for result in graphql_results[key]]
        rest_sizes = [result[1] for result in rest_results[key]]
        graphql_sizes = [result[1] for result in graphql_results[key]]

        response_sizes.append((key, sum(rest_sizes) / len(rest_sizes), sum(graphql_sizes) / len(graphql_sizes)))

        plt.figure(figsize=(14, 6))

        plt.subplot(1, 2, 1)
        plt.boxplot([rest_durations, graphql_durations], labels=['REST', 'GraphQL'])
        plt.title(f'Tempo de Resposta - {key}', fontsize=20)  
        plt.ylabel('Tempo de Resposta (s)', fontsize=16)  
        plt.xticks(fontsize=14) 
        plt.yticks(fontsize=14)  
        plt.tight_layout()
        plt.show()
    
    labels = [item[0] for item in response_sizes]
    rest_sizes_avg = [item[1] for item in response_sizes]
    graphql_sizes_avg = [item[2] for item in response_sizes]

    x = range(len(labels))

    plt.bar(x, rest_sizes_avg, width=0.4, label='REST', align='center')
    plt.bar(x, graphql_sizes_avg, width=0.4, label='GraphQL', align='edge')
    plt.xlabel('Tipo de Consulta', fontsize=16) 
    plt.ylabel('Tamanho Médio da Resposta (bytes)', fontsize=16)  
    plt.title('Comparação do Tamanho da Resposta entre REST e GraphQL', fontsize=20) 
    plt.xticks(ticks=x, labels=labels, fontsize=14)  
    plt.yticks(fontsize=14) 
    plt.legend(fontsize=14) 
    plt.tight_layout()
    plt.show()

def main():
    num_measurements = 10

    rest_results, graphql_results = run_tests(num_measurements)

    analyze_results(rest_results, graphql_results)

if __name__ == "__main__":
    main()
