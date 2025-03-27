from rest_service import app as rest_app
from grpc_service import serve as grpc_serve
from soap_service import start_soap_server
from graphql_service import start_graphql_server
from threading import Thread

if __name__ == "__main__":
    # Iniciar os serviços REST, gRPC, SOAP e GraphQL
    thread_rest = Thread(target=rest_app.run, kwargs={"host": "0.0.0.0", "port": 5000})
    thread_rest.start()

    thread_grpc = Thread(target=grpc_serve)
    thread_grpc.start()

    thread_soap = Thread(target=start_soap_server)
    thread_soap.start()

    thread_graphql = Thread(target=start_graphql_server)
    thread_graphql.start()
    
    # Manter o main.py em execução
    thread_rest.join()
    thread_grpc.join()
    thread_soap.join()
    thread_graphql.join()
