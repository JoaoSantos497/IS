import grpc
import tarefa_pb2
import tarefa_pb2_grpc

# Estabelecer uma conexão com o servidor gRPC
def criar_channel():
    return grpc.insecure_channel('localhost:50051')

def executar_servico(dados):
    channel = grpc.insecure_channel('localhost:50051')
    stub = tarefa_pb2_grpc.TarefaServiceStub(channel)

    # Supondo que os dados tenham os campos necessários para o serviço
    request = tarefa_pb2.TarefaRequest(titulo=dados["titulo"], descricao=dados["descricao"])
    response = stub.CriarTarefa(request)

    return {"message": response.message}

# Listar tarefas
def listar_tarefas():
    try:
        channel = grpc.insecure_channel('localhost:50051')
        stub = tarefa_pb2_grpc.TarefaStub(channel)
        response = stub.ListarTarefas(tarefa_pb2.ListarTarefasRequest())
        return response.tarefas
    except grpc.RpcError as e:
        print(f"Erro ao listar tarefas via gRPC: {e}")
        return []

# Criar uma nova tarefa
def criar_tarefa(stub, titulo, descricao, estado, data_limite):
    try:
        request = tarefa_pb2.CriarTarefaRequest(
            titulo=titulo,
            descricao=descricao,
            estado=estado,
            data_limite=data_limite
        )
        response = stub.CriarTarefa(request)
        print(f"Tarefa criada com sucesso! ID: {response.id}")
    except grpc.RpcError as e:
        print(f"Erro ao criar tarefa: {e}")

# Cliente principal
def main():
    # Estabelecer o canal de comunicação com o servidor
    channel = criar_channel()
    stub = tarefa_pb2_grpc.TarefaServiceStub(channel)

    # Exemplo: Listar tarefas
    listar_tarefas(stub)

    # Exemplo: Criar uma nova tarefa
    criar_tarefa(stub, "Nova Tarefa", "Descrição da nova tarefa", "Em andamento", "2025-05-01")

    # Listar novamente para verificar a criação
    listar_tarefas(stub)

if __name__ == '__main__':
    main()
