import requests
import json

# URL do servidor GraphQL
URL = 'http://127.0.0.1:4000/graphql'

def executar_query(query):
    payload = {"query": query}
    response = requests.post(URL, json=payload)
    return response.json()

# Função para listar tarefas
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
    url = 'http://127.0.0.1:4000/graphql'
    headers = {"Content-Type": "application/json"}
    response = requests.post(url, json={'query': query}, headers=headers)
    
    if response.status_code == 200:
        return response.json().get('data', {}).get('tarefas', [])
    else:
        print(f"Erro ao listar tarefas via GraphQL: {response.status_code}")
        return []

# Função para criar uma nova tarefa
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
        'titulo': titulo,
        'descricao': descricao,
        'estado': estado,
        'data_limite': data_limite
    }

    # Enviar a solicitação para o servidor GraphQL
    response = requests.post(URL, json={'query': mutation, 'variables': variables})

    # Verificar o status da resposta
    if response.status_code != 200:
        print(f"Erro ao criar tarefa. Status Code: {response.status_code}, Response Text: {response.text}")
        return None

    try:
        # Verifique se a resposta é válida
        data = response.json()

        # Log para depuração: Mostrar a resposta completa
        print("Resposta completa da criação da tarefa:", json.dumps(data, indent=4))

        if data and 'data' in data and 'criarTarefa' in data['data']:
            tarefa = data['data']['criarTarefa']
            return tarefa
        else:
            print(f"Erro ao processar a tarefa: Resposta recebida não contém 'data' ou 'criarTarefa'. Dados recebidos: {json.dumps(data, indent=4)}")
            return None
    except ValueError as e:
        print(f"Erro ao processar a resposta JSON: {e}")
        return None

# Função para testar a conexão com o servidor
def testar_servidor():
    query = """
    query {
        tarefas {
            id
            titulo
            descricao
        }
    }
    """
    response = requests.post(URL, json={'query': query})
    if response.status_code == 200:
        print("Resposta de teste:", response.json())
    else:
        print(f"Erro ao testar o servidor. Status Code: {response.status_code}, Response Text: {response.text}")

# Exemplo de uso do cliente

# Testar conexão com o servidor
testar_servidor()

# Listar tarefas
tarefas = listar_tarefas()
if tarefas:
    print("Tarefas:")
    for tarefa in tarefas:
        print(f"ID: {tarefa['id']}, Título: {tarefa['titulo']}, Estado: {tarefa['estado']}")

# Criar uma nova tarefa
nova_tarefa = criar_tarefa('Nova Tarefa', 'Descrição da nova tarefa', 'Em andamento', '2025-05-01')
if nova_tarefa:
    print(f"Nova tarefa criada: {nova_tarefa}")