from spyne import Application, rpc, ServiceBase, Unicode, Iterable
from spyne.protocol.soap import Soap11
from spyne.server.wsgi import WsgiApplication
from lxml import etree
import os
import uuid
import xmltodict

DADOS_XML = './dados/tarefas.xml'
XSD_PATH = './schema/tarefa.xsd'

def carregar_tarefas():
    if not os.path.exists(DADOS_XML):
        print("DEBUG: Nao existe:")
        return []
    with open(DADOS_XML) as f:
        print("DEBUG: Existe:")
        obj = xmltodict.parse(f.read())
        tarefas = obj.get('tarefas', {}).get('tarefa', [])
        if isinstance(tarefas, dict):
            return [tarefas]
        return tarefas

def guardar_tarefas(tarefas):
    xml = xmltodict.unparse({'tarefas': {'tarefa': tarefas}}, pretty=True)
    with open(DADOS_XML, 'w') as f:
        f.write(xml)

def validar_xml(xml_str):
    xmlschema_doc = etree.parse(XSD_PATH)
    xmlschema = etree.XMLSchema(xmlschema_doc)
    doc = etree.fromstring(xml_str.encode())
    xmlschema.assertValid(doc)

class TarefaService(ServiceBase):

    @rpc(_returns=Iterable(Unicode))
    def listar_tarefas(ctx):
        print("DEBUG: tarefas carregadas:")
        tarefas = carregar_tarefas()
        print(tarefas)
        for t in tarefas:
            yield str(t)

    @rpc(Unicode, Unicode, Unicode, Unicode, Unicode, _returns=Unicode)
    def criar_tarefa(ctx, titulo, descricao, estado, data_criacao, data_limite):
        nova = {
            'id': str(uuid.uuid4()),
            'titulo': titulo,
            'descricao': descricao,
            'estado': estado,
            'data_criacao': data_criacao,
            'data_limite': data_limite
        }
        tarefas = carregar_tarefas()
        tarefas.append(nova)
        guardar_tarefas(tarefas)
        return "Tarefa criada com sucesso"

app = Application([TarefaService],
                  tns='soap.tarefas',
                  in_protocol=Soap11(),
                  out_protocol=Soap11())

wsgi_app = WsgiApplication(app)

if __name__ == '__main__':
    from wsgiref.simple_server import make_server
    print("SOAP service a correr em http://192.168.246.23:8000")
    make_server('192.168.246.23', 8000, wsgi_app).serve_forever()
