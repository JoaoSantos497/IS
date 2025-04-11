import grpc
from concurrent import futures
import uuid
from datetime import datetime
import os
import json
import tarefa_pb2
import tarefa_pb2_grpc
from google.protobuf.empty_pb2 import Empty

DADOS_JSON = '/dados/tarefas.json'

# Carregar e guardar tarefas
def carregar_tarefas():
    if os.path.exists(DADOS_JSON):
        with open(DADOS_JSON) as f:
            return json.load(f)
    return []

def guardar_tarefas(tarefas):
    with open(DADOS_JSON, 'w') as f:
        json.dump(tarefas, f, indent=2)

# Implementação do serviço gRPC
class TarefaService(tarefa_pb2_grpc.TarefaServiceServicer):
    
    def ListarTarefas(self, request, context):
        tarefas = carregar_tarefas()
        return tarefa_pb2.TarefaList(tarefas=[tarefa_pb2.Tarefa(id=t['id'], 
                                                              titulo=t['titulo'],
                                                              descricao=t['descricao'],
                                                              estado=t['estado'],
                                                              data_criacao=t['data_criacao'],
                                                              data_limite=t['data_limite']) 
                                             for t in tarefas])

    def CriarTarefa(self, request, context):
        nova = {
            "id": str(uuid.uuid4()),
            "titulo": request.titulo,
            "descricao": request.descricao,
            "estado": request.estado,
            "data_criacao": datetime.now().strftime("%Y-%m-%d"),
            "data_limite": request.data_limite
        }
        tarefas = carregar_tarefas()
        tarefas.append(nova)
        guardar_tarefas(tarefas)
        return tarefa_pb2.Tarefa(id=nova['id'], 
                                 titulo=nova['titulo'], 
                                 descricao=nova['descricao'], 
                                 estado=nova['estado'], 
                                 data_criacao=nova['data_criacao'], 
                                 data_limite=nova['data_limite'])

    def CriarTarefaStream(self, request_iterator, context):
        tarefas = carregar_tarefas()
        for request in request_iterator:
            nova = {
                "id": str(uuid.uuid4()),
                "titulo": request.titulo,
                "descricao": request.descricao,
                "estado": request.estado,
                "data_criacao": datetime.now().strftime("%Y-%m-%d"),
                "data_limite": request.data_limite
            }
            tarefas.append(nova)
        guardar_tarefas(tarefas)
        return tarefa_pb2.TarefaList(tarefas=[tarefa_pb2.Tarefa(id=t['id'], 
                                                              titulo=t['titulo'],
                                                              descricao=t['descricao'],
                                                              estado=t['estado'],
                                                              data_criacao=t['data_criacao'],
                                                              data_limite=t['data_limite']) 
                                             for t in tarefas])

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    tarefa_pb2_grpc.add_TarefaServiceServicer_to_server(TarefaService(), server)
    server.add_insecure_port('[::]:50051')
    print("gRPC Server running on port 50051")
    server.start()
    server.wait_for_termination()

if __name__ == '__main__':
    serve()
