from spyne import Application, rpc, ServiceBase, Integer, Unicode  
from spyne.protocol.soap import Soap11  
from spyne.server.wsgi import WsgiApplication  
from wsgiref.simple_server import make_server  

class UserService(ServiceBase):  
    @rpc(Integer, Unicode, _returns=Unicode)  
    def add_user(ctx, user_id, name):  
        return f"Utilizador {name} (ID: {user_id}) adicionado com sucesso!"  

application = Application([UserService], 'soap.service.example', in_protocol=Soap11(), out_protocol=Soap11())  
wsgi_app = WsgiApplication(application)  

if __name__ == "__main__":  
    server = make_server('0.0.0.0', 8001, wsgi_app)  
    print("Servidor SOAP em http://0.0.0.0:8001")  
    server.serve_forever()
