import requests
from zeep import Client
import grpc
import json
import chat_pb2
import chat_pb2_grpc
from graphql_client import graphql_query
from rest_client import send_message_rest, create_group_rest, get_messages_rest
from grpc_client import send_message_grpc
from soap_client import send_message_soap

# Configurações
rest_url = "http://localhost:5000"
grpc_channel = grpc.insecure_channel('localhost:50051')
graphql_url = "http://localhost:5002/graphql"
soap_client = Client('http://localhost:8000/?wsdl')

# Funções para interagir com cada serviço
def create_group(group_name):
    create_group_rest(rest_url, group_name)

def send_message(group_name, message):
    send_message_rest(rest_url, group_name, message)
    send_message_grpc(grpc_channel, group_name, message)
    send_message_soap(soap_client, group_name, message)

def get_messages(group_name):
    print("REST:", get_messages_rest(rest_url, group_name))
    print("GraphQL:", graphql_query(graphql_url, group_name))

# Exemplos
create_group("Grupo1")
send_message("Grupo1", "Olá, grupo!")
get_messages("Grupo1")
