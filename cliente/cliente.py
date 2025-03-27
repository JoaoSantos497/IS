import requests
import grpc
import zeep
import json

from grpc_service import user_pb2, user_pb2_grpc

# Endpoints dos serviços
SOAP_URL = "http://localhost:8001/?wsdl"
REST_URL = "http://localhost:8002/users"
GRAPHQL_URL = "http://localhost:8003/graphql"
GRPC_HOST = "localhost:8004"

### 1️⃣ Cliente SOAP ###
def get_user_soap(user_id):
    client = zeep.Client(wsdl=SOAP_URL)
    response = client.service.GetUser(user_id)
    print("SOAP Response:", response)

### 2️⃣ Cliente REST ###
def get_user_rest(user_id):
    response = requests.get(f"{REST_URL}/{user_id}")
    print("REST Response:", response.json())

### 3️⃣ Cliente GraphQL ###
def get_user_graphql(user_id):
    query = """
    query GetUser($id: Int!) {
        getUser(id: $id) {
            id
            name
        }
    }
    """
    variables = {"id": user_id}
    response = requests.post(GRAPHQL_URL, json={"query": query, "variables": variables})
    print("GraphQL Response:", response.json())

### 4️⃣ Cliente gRPC ###
def get_user_grpc(user_id):
    with grpc.insecure_channel(GRPC_HOST) as channel:
        stub = user_pb2_grpc.UserServiceStub(channel)
        request = user_pb2.UserRequest(id=user_id)
        response = stub.GetUser(request)
        print("gRPC Response:", response)

### Testar todos os serviços ###
if __name__ == "__main__":
    user_id = 1  # ID de teste
    
    print("\n📌 Testando SOAP...")
    get_user_soap(user_id)

    print("\n📌 Testando REST...")
    get_user_rest(user_id)

    print("\n📌 Testando GraphQL...")
    get_user_graphql(user_id)

    print("\n📌 Testando gRPC...")
    get_user_grpc(user_id)
