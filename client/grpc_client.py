import grpc
import tarefa_pb2
import tarefa_pb2_grpc

def criar_channel():
    return grpc.insecure_channel('localhost:5001')

def listar_tarefas():
    try:
        channel = criar_channel()
        stub = tarefa_pb2_grpc.TarefaServiceStub(channel)
        response = stub.ListarTarefas(tarefa_pb2.Empty())
        
        # Debug: Verificar os dados recebidos
        for tarefa in response.tarefas:
            print(f"Tarefa: {tarefa.id}, {tarefa.titulo}, {tarefa.data_criacao}, {tarefa.data_limite}")

        # Convertendo as tarefas para dicionário para funcionar com o template
        return [
            {
                "id": t.id,
                "titulo": t.titulo,
                "descricao": t.descricao,
                "estado": t.estado,
                "data_criacao": t.data_criacao,  # Incluindo a data de criação para exibir no template
                "data_limite": t.data_limite     # Incluindo a data limite para exibir no template
            } for t in response.tarefas
        ]
    except grpc.RpcError as e:
        print(f"Erro ao listar tarefas via gRPC: {e}")
        return []

def criar_tarefa(titulo, descricao, estado, data_limite):
    try:
        channel = criar_channel()
        stub = tarefa_pb2_grpc.TarefaServiceStub(channel)
        
        # Criando a requisição para criar tarefa diretamente com Tarefa
        request = tarefa_pb2.Tarefa(
            titulo=titulo,
            descricao=descricao,
            estado=estado,
            data_limite=data_limite
        )
        
        # Chamando o método CriarTarefa do servidor gRPC
        response = stub.CriarTarefa(request)
        
        # Retornando a tarefa criada com seu id e outros campos
        return {
            "id": response.id,
            "titulo": response.titulo,
            "descricao": response.descricao,
            "estado": response.estado,
            "data_criacao": response.data_criacao,
            "data_limite": response.data_limite
        }
    except grpc.RpcError as e:
        print(f"Erro ao criar tarefa via gRPC: {e}")
        return {}

# Caso precise de uma interface genérica para execução
def executar_servico(dados):
    return criar_tarefa(
        titulo=dados["titulo"],
        descricao=dados["descricao"],
        estado=dados["estado"],
        data_limite=dados["data_limite"]
    )
