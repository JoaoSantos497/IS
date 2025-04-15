import requests

BASE_URL = "http://localhost:5000/tarefas/rest"

def listar_tarefas():
    try:
        response = requests.get('http://127.0.0.1:5000/tarefas')
        response.raise_for_status()  # Verifica se a requisição foi bem-sucedida
        return response.json()
    except requests.exceptions.HTTPError as err:
        print(f"Erro ao listar tarefas via REST: {err}")
        return []

def criar_tarefa(dados):
    try:
        response = requests.post('http://127.0.0.1:5000/tarefas', json=dados)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.HTTPError as err:
        print(f"Erro ao criar tarefa via REST: {err}")
        return {}

def atualizar_tarefa(id, titulo, descricao, estado, data_limite):
    tarefa = {
        "titulo": titulo,
        "descricao": descricao,
        "estado": estado,
        "data_limite": data_limite
    }
    response = requests.put(f"{BASE_URL}/{id}", json=tarefa)
    if response.status_code == 200:
        print("Tarefa atualizada com sucesso!")
    else:
        print(f"Erro ao atualizar tarefa: {response.text}")

def deletar_tarefa(id):
    response = requests.delete(f"{BASE_URL}/{id}")
    if response.status_code == 200:
        print("Tarefa deletada com sucesso!")
    else:
        print(f"Erro ao deletar tarefa: {response.text}")
