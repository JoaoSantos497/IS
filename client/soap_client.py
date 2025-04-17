import zeep
import requests
import json

URL = "http://localhost:8002/soap?wsdl"
client = zeep.Client(URL)

def listar_tarefas():
    try:
        resposta = client.service.listar_tarefas()
        print("SOAP retorno bruto:", resposta)

        tarefas = []

        if isinstance(resposta, list):
            for tarefa in resposta:
                try:
                    # Tenta converter JSON válido
                    tarefas.append(json.loads(tarefa))
                except json.JSONDecodeError:
                    # Tenta converter dicionário em string com aspas simples (formato Python)
                    import ast
                    tarefas.append(ast.literal_eval(tarefa))
        elif isinstance(resposta, str):
            # Caso único: resposta é uma string JSON representando uma lista
            tarefas = json.loads(resposta)
        elif isinstance(resposta, dict):
            tarefas = [resposta]
        else:
            print("Formato inesperado da resposta SOAP")

        return tarefas
    
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
