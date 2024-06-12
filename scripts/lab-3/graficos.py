import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import os

# Função para filtrar os dados de acordo com os critérios especificados
def filtrar_dados(df):
    df = df[(df['Merged'] == True) | (df['Closed'] == True)]
    return df

# Função para remover outliers usando o método IQR
def remove_outliers_iqr(df, column):
    Q1 = df[column].quantile(0.25)
    Q3 = df[column].quantile(0.75)
    IQR = Q3 - Q1
    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR
    return df[(df[column] >= lower_bound) & (df[column] <= upper_bound)]

diretorio_dados = "./scripts/lab-3/dataset/"
diretorio_graficos = "./scripts/lab-3/graficos/"

dfs = []

for arquivo in os.listdir(diretorio_dados):
    if arquivo.endswith(".csv") and arquivo not in ['out.csv', 'linux_prs.csv']:
        df = pd.read_csv(os.path.join(diretorio_dados, arquivo))
        if not df.empty and 'TimeToMergeOrClose' in df.columns:
            df = filtrar_dados(df)
            dfs.append(df)
        else:
            print(f"Arquivo {arquivo} está vazio ou não contém a coluna necessária. Pulando para o próximo arquivo.")

if len(dfs) == 0:
    print("Nenhum arquivo CSV válido encontrado.")
    exit()

df_concatenado = pd.concat(dfs, ignore_index=True)

print("Dataset Consolidado:")
print(df_concatenado)

metricas = ['Body', 'Additions', 'Deletions', 'ReviewComments', 'Participants', 'Comments', 'TimeToMergeOrClose']

# Corrigir os outliers
for coluna in metricas:
    df_concatenado = remove_outliers_iqr(df_concatenado, coluna)

# Salvar o gráfico de correlações
plt.figure(figsize=(10, 8))
sns.heatmap(df_concatenado[metricas].corr(), annot=True, cmap='coolwarm', fmt=".2f", linewidths=.5)
plt.title('Correlações entre as Métricas')
plt.savefig(os.path.join(diretorio_graficos, 'correlacoes.png'))
plt.show()

# A. Feedback Final das Revisões (Status do PR):

# RQ 01. Qual a relação entre o número de linhas adicionadas e o tempo para fechamento/merge?
plt.figure(figsize=(12, 6))
plt.subplot(1, 2, 1)
sns.scatterplot(x='Additions', y='TimeToMergeOrClose', data=df_concatenado[df_concatenado['Merged']], color='blue', alpha=0.5)
plt.title('Merged: Número de linhas adicionadas vs. Tempo para fechamento/merge')
plt.xlabel('Número de linhas adicionadas')
plt.ylabel('Tempo para fechamento/merge (em segundos)')

plt.subplot(1, 2, 2)
sns.scatterplot(x='Additions', y='TimeToMergeOrClose', data=df_concatenado[df_concatenado['Closed']], color='red', alpha=0.5)
plt.title('Closed: Número de linhas adicionadas vs. Tempo para fechamento/merge')
plt.xlabel('Número de linhas adicionadas')
plt.ylabel('Tempo para fechamento/merge (em segundos)')

plt.tight_layout()
plt.savefig(os.path.join(diretorio_graficos, 'relacao_additions_tempo.png'))
plt.show()

# RQ 02. Qual a relação entre o feedback final (Closed/Merged) e o tempo para fechamento/merge?
plt.figure(figsize=(8, 6))
sns.boxplot(x='Merged', y='TimeToMergeOrClose', data=df_concatenado)
plt.title('Relação entre o feedback final e o tempo para fechamento/merge')
plt.xlabel('Feedback Final')
plt.ylabel('Tempo para fechamento/merge (em segundos)')
plt.xticks([0, 1], ['Closed', 'Merged'])
plt.savefig(os.path.join(diretorio_graficos, 'relacao_feedback_tempo.png'))
plt.show()

# RQ 03. Qual a relação entre a descrição dos PRs e o feedback final das revisões?
plt.figure(figsize=(8, 6))
sns.boxplot(x='Merged', y='Comments', data=df_concatenado)
plt.title('Relação entre o feedback final e o número de comentários na descrição dos PRs')
plt.xlabel('Feedback Final')
plt.ylabel('Número de comentários na descrição dos PRs')
plt.xticks([0, 1], ['Closed', 'Merged'])
plt.savefig(os.path.join(diretorio_graficos, 'relacao_comments_feedback.png'))
plt.show()

# RQ 04. Qual a relação entre as interações nos PRs e o feedback final das revisões?
plt.figure(figsize=(8, 6))
sns.boxplot(x='Merged', y='Participants', data=df_concatenado)
plt.title('Relação entre o feedback final e o número de participantes nos PRs')
plt.xlabel('Feedback Final')
plt.ylabel('Número de participantes nos PRs')
plt.xticks([0, 1], ['Closed', 'Merged'])
plt.savefig(os.path.join(diretorio_graficos, 'relacao_participants_feedback.png'))
plt.show()

# B. Número de Revisões:

# RQ 05. Qual a relação entre o tamanho dos PRs e o número de revisões realizadas?
plt.figure(figsize=(8, 6))
sns.boxplot(x='Body', y='ReviewComments', data=df_concatenado)
plt.title('Relação entre o tamanho dos PRs e o número de revisões realizadas')
plt.xlabel('Tamanho dos PRs')
plt.ylabel('Número de revisões realizadas')
plt.savefig(os.path.join(diretorio_graficos, 'relacao_tamanho_revisoes.png'))
plt.show()

# RQ 06. Qual a relação entre o tempo de análise dos PRs e o número de revisões realizadas?
plt.figure(figsize=(8, 6))
sns.boxplot(x='TimeToMergeOrClose', y='ReviewComments', data=df_concatenado)
plt.title('Relação entre o tempo de análise dos PRs e o número de revisões realizadas')
plt.xlabel('Tempo de análise dos PRs (em segundos)')
plt.ylabel('Número de revisões realizadas')
plt.savefig(os.path.join(diretorio_graficos, 'relacao_tempo_analise_revisoes.png'))
plt.show()

# RQ 07. Qual a relação entre a descrição dos PRs e o número de revisões realizadas?
plt.figure(figsize=(8, 6))
sns.boxplot(x='Comments', y='ReviewComments', data=df_concatenado)
plt.title('Relação entre a descrição dos PRs e o número de revisões realizadas')
plt.xlabel('Número de comentários na descrição dos PRs')
plt.ylabel('Número de revisões realizadas')
plt.savefig(os.path.join(diretorio_graficos, 'relacao_comments_revisoes.png'))
plt.show()

# RQ 08. Qual a relação entre as interações nos PRs e o número de revisões realizadas?
plt.figure(figsize=(8, 6))
sns.boxplot(x='Participants', y='ReviewComments', data=df_concatenado)
plt.title('Relação entre as interações nos PRs e o número de revisões realizadas')
plt.xlabel('Número de participantes nos PRs')
plt.ylabel('Número de revisões realizadas')
plt.savefig(os.path.join(diretorio_graficos, 'relacao_participants_revisoes.png'))
plt.show()
