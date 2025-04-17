import zeep

URL = "http://localhost:8002/?wsdl"  # Corrigido: endpoint sem /soap
client = zeep.Client(URL)

def listar_tarefas():
    try:
        resposta = client.service.listar_tarefas()
        print("SOAP retorno bruto:", resposta)

        tarefas = []
        for tarefa in resposta:
            # Zeep retorna objetos tipo "zeep.objects.Tarefa", que podem ser convertidos em dict assim:
            tarefa_dict = {
                "id": tarefa.id,
                "titulo": tarefa.titulo,
                "descricao": tarefa.descricao,
                "estado": tarefa.estado,
                "data_criacao": tarefa.data_criacao,
                "data_limite": tarefa.data_limite
            }
            tarefas.append(tarefa_dict)

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

# (Opcional) exemplo de envio manual de XML SOAP, se necessário
def processar_requisicao(xml_data):
    import requests
    headers = {'Content-Type': 'text/xml'}  # SOAP 1.1 usa 'text/xml'
    response = requests.post("http://localhost:8002", data=xml_data, headers=headers)
    return response.text
