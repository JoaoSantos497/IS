import grpc
from concurrent import futures
import chat_pb2
import chat_pb2_grpc
from flask import jsonify
import json
import os

data_file = "data/chat_data.json"

def load_data():
    if os.path.exists(data_file):
        with open(data_file, "r", encoding="utf-8") as f:
            return json.load(f)
    return {"groups": {}}

def save_data(data):
    with open(data_file, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)

class ChatService(chat_pb2_grpc.ChatServicer):
    def SendMessage(self, request, context):
        data = load_data()
        if request.group_name not in data["groups"]:
            return chat_pb2.MessageResponse(status="Grupo não encontrado!")
        data["groups"][request.group_name]["messages"].append(request.message)
        save_data(data)
        return chat_pb2.MessageResponse(status="Mensagem enviada!")

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    chat_pb2_grpc.add_ChatServicer_to_server(ChatService(), server)
    server.add_insecure_port("[::]:50051")
    server.start()
    server.wait_for_termination()
