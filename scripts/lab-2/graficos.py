import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime

csv_path = "./scripts/sprint-2/dataset/s2_updated.csv"
df = pd.read_csv(csv_path)

df['createdAt'] = pd.to_datetime(df['createdAt']).dt.date

now = datetime.utcnow().date()  # Get current UTC date
df['age_years'] = (now - df['createdAt']).dt.days / 365.25

quality_metrics = ['CBO', 'DIT', 'LCOM', 'LOC']

process_metrics = {
    'Popularidade': 'stargazerCount',
    'Maturidade (anos)': 'age_years',
    'Atividade (releases)': 'commitCount',
    'Tamanho (LOC)': 'LOC',
    'Tamanho (Linhas de Comentários)': 'LCOM'
}

def plot_relationship(x_metric, y_metric):
    plt.scatter(df[x_metric], df[y_metric])
    plt.xlabel(x_metric)
    plt.ylabel(y_metric)
    plt.title(f'Relação entre {x_metric} e {y_metric}')
    plt.show()

def research_question(metric):
    print(f"Qual a relação entre {metric} e suas características de qualidade?")
    for quality_metric in quality_metrics:
        plot_relationship(metric, quality_metric)

for process_metric, process_metric_value in process_metrics.items():
    research_question(process_metric_value)
