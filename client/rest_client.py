import requests

BASE_URL = "http://localhost:8001/tarefas"


def listar_tarefas():
    try:
        response = requests.get(BASE_URL)
        response.raise_for_status()
        
        # Mostra o conteúdo bruto (útil para debug)
        print("Resposta bruta do servidor REST:", response.text)

        # Tenta converter para JSON
        return response.json()
    except requests.exceptions.HTTPError as err:
        print(f"Erro HTTP ao listar tarefas via REST: {err}")
    except ValueError as e:
        print(f"Erro ao decodificar JSON da resposta: {e}")
        print("Conteúdo retornado:", response.text)
    return []

def criar_tarefa(titulo, descricao, estado, data_limite):
    tarefa = {
        "titulo": titulo,
        "descricao": descricao,
        "estado": estado,
        "data_limite": data_limite
    }
    try:
        response = requests.post(BASE_URL, json=tarefa)
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
