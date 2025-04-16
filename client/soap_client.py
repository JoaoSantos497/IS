import zeep
import requests

URL = "http://localhost:8002/soap?wsdl"
client = zeep.Client(URL)

def listar_tarefas():
    try:
        return client.service.listar_tarefas()
    except Exception as e:
        print(f"Erro ao listar tarefas via SOAP: {e}")
        return []

def criar_tarefa(titulo, descricao, estado, data_criacao, data_limite):
    try:
        resposta = client.service.criar_tarefa(titulo, descricao, estado, data_criacao, data_limite)
        print("Resposta:", resposta)
        return resposta
    except Exception as e:
        print(f"Erro ao criar tarefa via SOAP: {e}")
        return None

# Exemplo para processar XML se necessário
def processar_requisicao(xml_data):
    headers = {'Content-Type': 'application/soap+xml'}
    response = requests.post(URL, data=xml_data, headers=headers)
    return response.text
