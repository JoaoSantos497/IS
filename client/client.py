import requests # type: ignore
import json
import zeep# type: ignore
from graphqlclient import GraphQLClient# type: ignore
import grpc# type: ignore
import tarefa_pb2# type: ignore
import tarefa_pb2_grpc# type: ignore
import xmltodict

# Função para interagir com o serviço REST
def client_rest():
    print("Interagindo com o serviço REST...")
    
    # GET - Listar tarefas
    response = requests.get('http://localhost:5000/tarefas')
    tarefas = response.json()
    print("Tarefas (REST):", tarefas)

    # POST - Criar tarefa
    nova_tarefa = {
        "titulo": "Nova Tarefa REST",
        "descricao": "Descrição da tarefa",
        "estado": "pendente",
        "data_limite": "2025-04-30"
    }
    response = requests.post('http://localhost:5000/tarefas', json=nova_tarefa)
    print("Tarefa Criada (REST):", response.json())

# Função para interagir com o serviço SOAP
def client_soap():
    print("Interagindo com o serviço SOAP...")
    
    # Criar cliente SOAP
    client = zeep.Client('http://localhost:5002/soap?wsdl')
    
    # Listar tarefas (exemplo)
    tarefas = client.service.ListarTarefas()
    print("Tarefas (SOAP):", tarefas)

    # Criar tarefa (exemplo)
    nova_tarefa = {
        "titulo": "Nova Tarefa SOAP",
        "descricao": "Descrição da tarefa",
        "estado": "pendente",
        "data_limite": "2025-04-30"
    }
    tarefa = client.service.CriarTarefa(**nova_tarefa)
    print("Tarefa Criada (SOAP):", tarefa)

# Função para interagir com o serviço GraphQL
def client_graphql():
    print("Interagindo com o serviço GraphQL...")
    
    client = GraphQLClient('http://localhost:5003/graphql')

    # Query para listar tarefas
    query = '{ listarTarefas { id titulo descricao estado dataCriacao dataLimite } }'
    response = client.execute(query)
    print("Tarefas (GraphQL):", response)

    # Mutation para criar tarefa
    mutation = '''
    mutation {
        criarTarefa(titulo: "Nova Tarefa GraphQL", descricao: "Descrição", estado: "pendente", dataLimite: "2025-04-30") {
            id
            titulo
            descricao
        }
    }
    '''
    response = client.execute(mutation)
    print("Tarefa Criada (GraphQL):", response)

# Função para interagir com o serviço gRPC
def client_grpc():
    print("Interagindo com o serviço gRPC...")
    
    channel = grpc.insecure_channel('localhost:50051')
    stub = tarefa_pb2_grpc.TarefaServiceStub(channel)

    # Listar tarefas
    response = stub.ListarTarefas(tarefa_pb2.Empty())
    print("Tarefas (gRPC):")
    for tarefa in response.tarefas:
        print(f"{tarefa.titulo}")

    # Criar tarefa
    nova_tarefa = stub.CriarTarefa(tarefa_pb2.Tarefa(
        titulo="Nova Tarefa gRPC", 
        descricao="Descrição da tarefa", 
        estado="pendente", 
        data_limite="2025-04-30"
    ))
    print(f"Tarefa Criada (gRPC): {nova_tarefa.titulo}")

# Função para exportar/importar dados JSON
def exportar_json():
    print("Exportando dados JSON...")
    response = requests.get('http://localhost:5000/export/json')
    print("Dados exportados (JSON):", response.json())

def importar_json():
    print("Importando dados JSON...")
    dados = [{"titulo": "Tarefa 1", "descricao": "Descrição 1", "estado": "pendente", "data_limite": "2025-04-30"}]
    response = requests.post('http://localhost:5000/import/json', json=dados)
    print("Dados importados (JSON):", response.json())

# Função para exportar/importar dados XML
def exportar_xml():
    print("Exportando dados XML...")
    response = requests.get('http://localhost:5000/export/xml')
    print("Dados exportados (XML):", response.text)

def importar_xml():
    print("Importando dados XML...")
    xml = '''<tarefas><tarefa><titulo>Tarefa 1</titulo><descricao>Descrição 1</descricao><estado>pendente</estado><data_limite>2025-04-30</data_limite></tarefa></tarefas>'''
    response = requests.post('http://localhost:5000/import/xml', data=xml)
    print("Dados importados (XML):", response.json())

# Função principal para executar todos os clientes
def main():
    client_rest()
    client_soap()
    client_graphql()
    client_grpc()
    exportar_json()
    importar_json()
    exportar_xml()
    importar_xml()

if __name__ == '__main__':
    main()