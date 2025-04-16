import subprocess
import os

def iniciar_servico(nome, caminho):
    return subprocess.Popen(["python3", caminho], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

if __name__ == "__main__":
    print("Inicializando os serviços...\n")

    # Garante que a pasta de dados existe
    os.makedirs("dados", exist_ok=True)
    if not os.path.exists("dados/tarefas.json"):
        with open("dados/tarefas.json", "w") as f:
            f.write("[]")

    # Lista de serviços a iniciar
    servicos = {
        "REST": "rest/app.py",
        "SOAP": "soap/app.py",
        "GraphQL": "graphql/app.py",
        "gRPC": "grpc/app.py"
    }

    processos = {}

    for nome, caminho in servicos.items():
        print(f"Iniciando {nome}...")
        processos[nome] = iniciar_servico(nome, caminho)

    print("\nTodos os serviços foram iniciados. Logs em tempo real:\n")

    try:
        # Mostrar logs dos serviços em tempo real
        while True:
            for nome, proc in processos.items():
                output = proc.stdout.readline()
                if output:
                    print(f"[{nome}] {output.decode().strip()}")
                if proc.poll() is not None:
                    print(f"[{nome}] terminou com código {proc.returncode}")
                    del processos[nome]
                    break
            if not processos:
                break
    except KeyboardInterrupt:
        print("\nEncerrando todos os serviços...")
        for proc in processos.values():
            proc.terminate()
