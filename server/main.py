import multiprocessing
import os
import time
import subprocess

def iniciar_rest():
    os.system("python3 rest/app.py")


def iniciar_soap():
    os.system("python3 soap/app.py")


def iniciar_graphql():
    os.system("python3 graphql/app.py")

def iniciar_grpc():
    os.system("python3 grpc/app.py")

if __name__ == "__main__":
    print("Inicializando os serviços...")

    # Garante que a pasta de dados existe
    os.makedirs("dados", exist_ok=True)
    if not os.path.exists("dados/tarefas.json"):
        with open("dados/tarefas.json", "w") as f:
            f.write("[]")

    # Iniciar cada serviço num processo separado
    processos = [
        multiprocessing.Process(target=iniciar_rest),
        multiprocessing.Process(target=iniciar_soap),
        multiprocessing.Process(target=iniciar_graphql),
        multiprocessing.Process(target=iniciar_grpc),
    ]

    for processo in processos:
        processo.start()

    for processo in processos:
        processo.join()