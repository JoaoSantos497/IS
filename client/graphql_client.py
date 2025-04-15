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
    url = 'http://127.0.0.1:5000/graphql'
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
            tarefa {
                id
                titulo
                descricao
                estado
                data_criacao
                data_limite
            }
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

        # Log para depuração
        print("Resposta completa da criação da tarefa:", data)

        if data and 'data' in data and 'criarTarefa' in data['data']:
            tarefa = data['data']['criarTarefa']['tarefa']
            return tarefa
        else:
            print(f"Erro ao processar a tarefa: Resposta recebida não contém 'data' ou 'criarTarefa'. Dados recebidos: {data}")
            return None
    except ValueError as e:
        print(f"Erro ao processar a resposta JSON: {e}")
        return None


# Exemplo de uso do cliente

# Listar tarefas
tarefas = listar_tarefas()
if tarefas:
    print("Tarefas:")
    for tarefa in tarefas:
        print(f"ID: {tarefa['id']}, Título: {tarefa['titulo']}, Estado: {tarefa['estado']}")

# Criar uma nova tarefa
nova_tarefa = criar_tarefa('Nova Tarefa', 'Descrição da nova tarefa', 'Em andamento', '2025-05-01')
if nova_tarefa:
    print("\nNova Tarefa Criada:")
    print(f"ID: {nova_tarefa['id']}, Título: {nova_tarefa['titulo']}, Estado: {nova_tarefa['estado']}")
