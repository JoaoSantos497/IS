import grpc
import tarefa_pb2
import tarefa_pb2_grpc

def criar_channel():
    return grpc.insecure_channel('localhost:5001')

def listar_tarefas():
    try:
        channel = criar_channel()
        stub = tarefa_pb2_grpc.TarefaServiceStub(channel)
        response = stub.ListarTarefas(tarefa_pb2.ListarTarefasRequest())
        return response.tarefas
    except grpc.RpcError as e:
        print(f"Erro ao listar tarefas via gRPC: {e}")
        return []

def criar_tarefa(titulo, descricao, estado, data_limite):
    try:
        channel = criar_channel()
        stub = tarefa_pb2_grpc.TarefaServiceStub(channel)
        request = tarefa_pb2.CriarTarefaRequest(
            titulo=titulo,
            descricao=descricao,
            estado=estado,
            data_limite=data_limite
        )
        response = stub.CriarTarefa(request)
        return {"id": response.id, "mensagem": response.message}
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
