import grpc
from concurrent import futures
import json
import os
import user_pb2
import user_pb2_grpc

DATA_FILE = "data/data.json"

def load_data():
    if not os.path.exists(DATA_FILE):
        return []
    with open(DATA_FILE, "r") as file:
        return json.load(file)

def save_data(data):
    with open(DATA_FILE, "w") as file:
        json.dump(data, file, indent=4)

class UserService(user_pb2_grpc.UserServiceServicer):
    def GetUser(self, request, context):
        data = load_data()
        user = next((u for u in data if u["id"] == request.id), None)
        if user:
            return user_pb2.UserResponse(id=user["id"], name=user["name"])
        context.abort(grpc.StatusCode.NOT_FOUND, "Utilizador não encontrado")

    def CreateUser(self, request, context):
        data = load_data()
        if any(u["id"] == request.id for u in data):
            context.abort(grpc.StatusCode.ALREADY_EXISTS, "ID já existe")
        new_user = {"id": request.id, "name": request.name}
        data.append(new_user)
        save_data(data)
        return user_pb2.UserResponse(id=new_user["id"], name=new_user["name"])

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    user_pb2_grpc.add_UserServiceServicer_to_server(UserService(), server)
    server.add_insecure_port("[::]:8004")
    print("Servidor gRPC na porta 8004")
    server.start()
    server.wait_for_termination()

if __name__ == "__main__":
    serve()
