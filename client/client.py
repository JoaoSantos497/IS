import sys
from graphqlclient import GraphQLClient
import requests
import zeep
import grpc
sys.path.append('../server/grpc')
import tarefa_pb2 # type: ignore
import tarefa_pb2_grpc # type: ignore

# Função para interagir com o serviço REST
def client_rest():
    print("\n[REST] Interagindo com o serviço REST...")

    # GET - Listar tarefas
    response = requests.get('http://localhost:5000/tarefas')
    tarefas = response.json()
    print("Tarefas:", tarefas)

    # POST - Criar tarefa
    nova_tarefa = {
        "titulo": "Nova Tarefa REST",
        "descricao": "Descrição da tarefa",
        "estado": "pendente",
        "data_limite": "2025-04-30"
    }
    response = requests.post('http://localhost:5000/tarefas', json=nova_tarefa)
    print("Tarefa Criada:", response.json())

# Função para interagir com o serviço SOAP
def client_soap():
    print("\n[SOAP] Interagindo com o serviço SOAP...")

    client = zeep.Client('http://localhost:5002/soap?wsdl')

    # Listar tarefas
    tarefas = client.service.ListarTarefas()
    print("Tarefas:", tarefas)

    # Criar tarefa
    nova_tarefa = {
        "titulo": "Nova Tarefa SOAP",
        "descricao": "Descrição da tarefa",
        "estado": "pendente",
        "data_limite": "2025-04-30"
    }
    tarefa = client.service.CriarTarefa(**nova_tarefa)
    print("Tarefa Criada:", tarefa)

# Função para interagir com o serviço GraphQL
def client_graphql():
    print("\n[GraphQL] Interagindo com o serviço GraphQL...")

    client = GraphQLClient('http://localhost:5003/graphql')

    # Query para listar tarefas
    query = '{ listarTarefas { id titulo descricao estado dataCriacao dataLimite } }'
    response = client.execute(query)
    print("Tarefas:", response)

    # Mutation para criar tarefa
    mutation = '''
    mutation {
        criarTarefa(titulo: \"Nova Tarefa GraphQL\", descricao: \"Descrição\", estado: \"pendente\", dataLimite: \"2025-04-30\") {
            id
            titulo
            descricao
        }
    }
    '''
    response = client.execute(mutation)
    print("Tarefa Criada:", response)

# Função para interagir com o serviço gRPC
def client_grpc():
    print("\n[gRPC] Interagindo com o serviço gRPC...")

    channel = grpc.insecure_channel('localhost:50051')
    stub = tarefa_pb2_grpc.TarefaServiceStub(channel)

    # Listar tarefas
    response = stub.ListarTarefas(tarefa_pb2.Empty())
    print("Tarefas:")
    for tarefa in response.tarefas:
        print(f"- {tarefa.titulo} ({tarefa.estado})")

    # Criar tarefa
    nova_tarefa = stub.CriarTarefa(tarefa_pb2.Tarefa(
        titulo="Nova Tarefa gRPC",
        descricao="Descrição da tarefa",
        estado="pendente",
        data_limite="2025-04-30"
    ))
    print("Tarefa Criada:", nova_tarefa.titulo)

# Função para exportar/importar dados JSON
def exportar_json():
    print("\n[JSON] Exportando dados...")
    response = requests.get('http://localhost:5000/export/json')
    print("Exportado:", response.json())

def importar_json():
    print("\n[JSON] Importando dados...")
    dados = [{"titulo": "Tarefa 1", "descricao": "Descrição 1", "estado": "pendente", "data_limite": "2025-04-30"}]
    response = requests.post('http://localhost:5000/import/json', json=dados)
    print("Importado:", response.json())

# Função para exportar/importar dados XML
def exportar_xml():
    print("\n[XML] Exportando dados...")
    response = requests.get('http://localhost:5000/export/xml')
    print("Exportado:", response.text)

def importar_xml():
    print("\n[XML] Importando dados...")
    xml = '''<tarefas><tarefa><titulo>Tarefa 1</titulo><descricao>Descrição 1</descricao><estado>pendente</estado><data_limite>2025-04-30</data_limite></tarefa></tarefas>'''
    headers = {'Content-Type': 'application/xml'}
    response = requests.post('http://localhost:5000/import/xml', data=xml, headers=headers)
    print("Importado:", response.json())

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
