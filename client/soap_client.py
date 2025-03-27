from zeep import Client

def send_message_soap(client, group_name, message):
    service = client.bind('ChatService', 'http://www.w3.org/2003/05/soap-envelope')
    response = service.send_message(group_name, message)
    print(f"Mensagem enviada via SOAP: {response}")
