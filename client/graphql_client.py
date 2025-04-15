from graphqlclient import GraphQLClient
import json

client = GraphQLClient('http://127.0.0.1:4000/graphql')

def listar_tarefas():
    query = '''
    {
        listarTarefas {
            id
            titulo
            descricao
            estado
            dataLimite
        }
    }
    '''
    try:
        response = client.execute(query)
        data = json.loads(response)
        return data['data']['listarTarefas']
    except Exception as e:
        print(f"Erro ao listar tarefas (GraphQL): {e}")
        return []

def criar_tarefa(titulo, descricao, estado, data_limite):
    mutation = f'''
    mutation {{
        criarTarefa(titulo: "{titulo}", descricao: "{descricao}", estado: "{estado}", dataLimite: "{data_limite}") {{
            id
            titulo
            descricao
            estado
            dataLimite
        }}
    }}
    '''
    try:
        response = client.execute(mutation)
        data = json.loads(response)
        return data['data']['criarTarefa']
    except Exception as e:
        print(f"Erro ao criar tarefa (GraphQL): {e}")
        return None
