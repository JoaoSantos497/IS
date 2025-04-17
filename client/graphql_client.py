import requests
import json

URL = "http://localhost:8003/graphql"

def executar_query(query, variables=None):
    payload = {"query": query}
    if variables:
        payload["variables"] = variables
    response = requests.post(URL, json=payload)
    return response.json()

def listar_tarefas():
    query = """
    query {
        tarefas {
            id
            titulo
            descricao
            estado
            dataLimite
            dataCriacao
        }
    }
    """
    data = executar_query(query)
    tarefas = data.get('data', {}).get('tarefas', [])
    print("Tarefas retornadas:", tarefas)
    return tarefas
    ##return data.get('data', {}).get('tarefas', [])

def criar_tarefa(titulo, descricao, estado, dataLimite):
    mutation = """
    mutation($titulo: String!, $descricao: String!, $estado: String!, $dataLimite: String!) {
        criarTarefa(titulo: $titulo, descricao: $descricao, estado: $estado, dataLimite: $dataLimite) {
            id
            titulo
            descricao
            estado
            dataCriacao
            dataLimite
        }
    }
    """
    variables = {
        "titulo": titulo,
        "descricao": descricao,
        "estado": estado,
        "dataLimite": dataLimite
    }
    data = executar_query(mutation, variables)
    return data.get('data', {}).get('criarTarefa', None)
