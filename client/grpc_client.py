import grpc
import chat_pb2
import chat_pb2_grpc

def send_message_grpc(channel, group_name, message):
    stub = chat_pb2_grpc.ChatStub(channel)
    request = chat_pb2.MessageRequest(group_name=group_name, message=message)
    response = stub.SendMessage(request)
    print(f"Mensagem enviada via gRPC: {response.status}")
