import zeep
import requests

# URL do serviço SOAP
URL = 'http://127.0.0.1:8000/soap?wsdl'

# Só para debug: ver operações disponíveis
client = zeep.Client(URL)
print("Operações disponíveis no WSDL:")
for service in client.wsdl.services.values():
    for port in service.ports.values():
        operations = port.binding._operations
        for op in operations:
            print(f" - {op}")

def processar_requisicao(xml_data):
    headers = {'Content-Type': 'application/soap+xml'}
    response = requests.post(URL, data=xml_data, headers=headers)
    return response.text

# Função para listar tarefas
def listar_tarefas():
    try:
        # Cria o cliente SOAP com o WSDL
        client = zeep.Client(URL)
        
        # Aqui, altere para a operação correta de acordo com o WSDL
        tarefas = client.service.listar_tarefas()  # Substitua pelo nome da operação do WSDL
        return tarefas
    except Exception as e:
        print(f"Erro ao listar tarefas via SOAP: {e}")
        return []

# Função para criar uma nova tarefa
def criar_tarefa(titulo, descricao, estado, data_criacao, data_limite):
    # Criando um cliente SOAP
    client = zeep.Client(URL)
    
    # Chamando o método criar_tarefa do serviço SOAP
    resposta = client.service.criar_tarefa(titulo, descricao, estado, data_criacao, data_limite)
    
    print(resposta)

# Exemplo de uso do cliente

# Listar tarefas
listar_tarefas()

# Criar uma nova tarefa
criar_tarefa('Nova Tarefa SOAP', 'Descrição da tarefa SOAP', 'Em andamento', '2025-04-20', '2025-05-01')

# Listar tarefas novamente para confirmar que a nova tarefa foi criada
listar_tarefas()
