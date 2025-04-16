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
            data_limite
        }
    }
    """
    data = executar_query(query)
    return data.get('data', {}).get('tarefas', [])

def criar_tarefa(titulo, descricao, estado, data_limite):
    mutation = """
    mutation($titulo: String!, $descricao: String!, $estado: String!, $data_limite: String!) {
        criarTarefa(titulo: $titulo, descricao: $descricao, estado: $estado, data_limite: $data_limite) {
            id
            titulo
            descricao
            estado
            data_criacao
            data_limite
        }
    }
    """
    variables = {
        "titulo": titulo,
        "descricao": descricao,
        "estado": estado,
        "data_limite": data_limite
    }
    data = executar_query(mutation, variables)
    return data.get('data', {}).get('criarTarefa', None)
