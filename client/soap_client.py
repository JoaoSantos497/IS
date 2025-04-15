import zeep

# Define o cliente SOAP com o WSDL do servidor
client = zeep.Client('http://localhost:5000/soap?wsdl')

def listar_tarefas():
    try:
        # Chama o método ListarTarefas do serviço SOAP
        tarefas = client.service.ListarTarefas()
        # Processa a resposta, caso necessário
        return tarefas
    except Exception as e:
        print(f"Erro ao listar tarefas (SOAP): {e}")
        return []

def criar_tarefa(titulo, descricao, estado, data_limite):
    try:
        # Chama o método CriarTarefa do serviço SOAP
        tarefa = client.service.CriarTarefa(
            titulo=titulo,
            descricao=descricao,
            estado=estado,
            data_limite=data_limite
        )
        # Retorna a tarefa criada ou algum identificador
        return tarefa
    except Exception as e:
        print(f"Erro ao criar tarefa (SOAP): {e}")
        return None
