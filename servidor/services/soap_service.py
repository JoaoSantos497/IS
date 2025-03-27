from spyne import Application, rpc, ServiceBase
from spyne.protocol.soap import Soap11
from spyne.server.wsgi import WsgiApplication
from wsgiref.simple_server import make_server

class ChatService(ServiceBase):
    @rpc(str, str, _returns=str)
    def send_message(ctx, group_name, message):
        # Lógica para enviar mensagem ao grupo
        return "Mensagem enviada com sucesso!"

def start_soap_server():
    soap_app = Application([ChatService], tns='tns.chat', in_protocol=Soap11(), out_protocol=Soap11())
    wsgi_app = WsgiApplication(soap_app)
    server = make_server('0.0.0.0', 8000, wsgi_app)
    server.serve_forever()
