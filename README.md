
# LAB <XX> : Sprint 01

## Enunciado:

Lab01S01: Consulta graphql para 100 repositórios (com todos os dados/métricas necessários para responder as RQs) + requisição automática (3 pontos)
### Questões

RQ 01. Sistemas populares são maduros/antigos?

Métrica: idade do repositório (calculado a partir da data de sua criação)

RQ 02. Sistemas populares recebem muita contribuição externa?

Métrica: total de pull requests aceitas

RQ 03. Sistemas populares lançam releases com frequência?

Métrica: total de releases

RQ 04. Sistemas populares são atualizados com frequência?

Métrica: tempo até a última atualização (calculado a partir da data de última atualização)

RQ 05. Sistemas populares são escritos nas [linguagens mais populares](https://octoverse.github.com/).?

Métrica: linguagem primária de cada um desses repositórios

RQ 06. Sistemas populares possuem um alto percentual de issues fechadas?

Métrica: razão entre número de issues fechadas pelo total de issues
## Integrantes do grupo:

* Ana Flávia de Souza Ribeiro
* Elian Eliezer Fialho de Castro
* Miguel Martins Fonseca da Cruz
* Rafael Augusto Vieira de Almeida

## Artefatos:

* [Relatório](docs/README.md)
* [Scripts](scripts)
* [Conjunto de dados](scripts/dataset)
  


## Como rodar
No diretório raíz(este) execute `python3 ./scripts/sprint-1/RQ01.py`