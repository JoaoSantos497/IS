import requests
import json

URL = 'http://127.0.0.1:5000'

def listar_tarefas():
    try:
        # Realiza a requisição GET para listar as tarefas
        response = requests.get(f'{URL}/tarefas')
        response.raise_for_status()  # Levanta um erro para status codes 4xx/5xx
        # Retorna as tarefas como JSON
        return response.json()
    except requests.exceptions.HTTPError as errh:
        print(f"Erro HTTP ao listar tarefas: {errh}")
        return []
    except requests.exceptions.RequestException as err:
        print(f"Erro ao realizar a requisição para listar tarefas: {err}")
        return []

def criar_tarefa(titulo, descricao, estado, data_limite):
    payload = {
        "titulo": titulo,
        "descricao": descricao,
        "estado": estado,
        "data_limite": data_limite
    }
    try:
        # Realiza a requisição POST para criar uma nova tarefa
        response = requests.post(f'{URL}/tarefas', json=payload)
        response.raise_for_status()  # Levanta um erro para status codes 4xx/5xx
        # Retorna a tarefa criada como JSON
        return response.json()
    except requests.exceptions.HTTPError as errh:
        print(f"Erro HTTP ao criar tarefa: {errh}")
        return None
    except requests.exceptions.RequestException as err:
        print(f"Erro ao realizar a requisição para criar tarefa: {err}")
        return None
