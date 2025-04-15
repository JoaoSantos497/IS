import grpc
import tarefa_pb2
import tarefa_pb2_grpc

def listar_tarefas():
    try:
        # Estabelece o canal com o servidor
        channel = grpc.insecure_channel('127.0.0.1:50051')
        stub = tarefa_pb2_grpc.TarefaServiceStub(channel)
        
        # Chama o método ListarTarefas e pega a resposta
        response = stub.ListarTarefas(tarefa_pb2.Empty())
        
        # Converte a resposta para um formato de lista de dicionários
        tarefas = []
        for t in response.tarefas:
            tarefas.append({
                "id": t.id,
                "titulo": t.titulo,
                "descricao": t.descricao,
                "estado": t.estado,
                "data_limite": t.data_limite
            })
        return tarefas
    except grpc.RpcError as e:
        print(f"Erro gRPC ao listar tarefas: {e}")
        return []
    except Exception as e:
        print(f"Erro inesperado ao listar tarefas: {e}")
        return []

def criar_tarefa(titulo, descricao, estado, data_limite):
    try:
        # Estabelece o canal com o servidor
        channel = grpc.insecure_channel('127.0.0.1:50051')
        stub = tarefa_pb2_grpc.TarefaServiceStub(channel)
        
        # Cria a tarefa com os parâmetros fornecidos
        tarefa = tarefa_pb2.Tarefa(
            titulo=titulo,
            descricao=descricao,
            estado=estado,
            data_limite=data_limite
        )
        
        # Chama o método CriarTarefa e recebe a resposta
        response = stub.CriarTarefa(tarefa)
        
        # Retorna os dados da tarefa criada
        return {
            "id": response.id,
            "titulo": response.titulo,
            "descricao": response.descricao,
            "estado": response.estado,
            "data_limite": response.data_limite
        }
    except grpc.RpcError as e:
        print(f"Erro gRPC ao criar tarefa: {e}")
        return None
    except Exception as e:
        print(f"Erro inesperado ao criar tarefa: {e}")
        return None
