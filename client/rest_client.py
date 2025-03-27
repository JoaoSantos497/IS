import requests

def create_group_rest(url, group_name):
    response = requests.post(f"{url}/groups", json={"group_name": group_name})
    if response.status_code == 200:
        print(f"Grupo '{group_name}' criado com sucesso.")
    else:
        print(f"Erro ao criar grupo: {response.json()}")

def send_message_rest(url, group_name, message):
    response = requests.post(f"{url}/groups/{group_name}/messages", json={"message": message})
    if response.status_code == 200:
        print("Mensagem enviada via REST.")
    else:
        print(f"Erro ao enviar mensagem: {response.json()}")

def get_messages_rest(url, group_name):
    response = requests.get(f"{url}/groups/{group_name}/messages")
    if response.status_code == 200:
        return response.json()
    else:
        return response.json()
