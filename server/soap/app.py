from spyne import Application, rpc, ServiceBase, Unicode, Iterable, ComplexModel
from spyne.protocol.soap import Soap11
from spyne.server.wsgi import WsgiApplication
from lxml import etree
import os
import uuid
import xmltodict
import json

# Caminhos
DADOS_JSON = '../dados/tarefas.json'
XSD_PATH = './schema/tarefa.xsd'

# --- Funções auxiliares ---

def carregar_tarefas():
    if os.path.exists(DADOS_JSON):
        with open(DADOS_JSON) as f:
            return json.load(f)
    return []

def guardar_tarefas(tarefas):
    with open(DADOS_JSON, 'w') as f:
        json.dump(tarefas, f, indent=2)

def validar_com_xsd(tarefa_dict):
    xml_temp = xmltodict.unparse({'tarefa': tarefa_dict}, pretty=True)
    xmlschema_doc = etree.parse(XSD_PATH)
    xmlschema = etree.XMLSchema(xmlschema_doc)
    doc = etree.fromstring(xml_temp.encode())
    xmlschema.assertValid(doc)

# --- Serviço SOAP ---

class Tarefa(ComplexModel):
    id = Unicode
    titulo = Unicode
    descricao = Unicode
    estado = Unicode
    data_criacao = Unicode
    data_limite = Unicode
    
class TarefaService(ServiceBase):

    @rpc(_returns=Iterable(Tarefa))
    def listar_tarefas(ctx):
        tarefas_json = carregar_tarefas()
        tarefas = []
        for t in tarefas_json:
            tarefa = Tarefa(
                id=t.get('id', ''),
                titulo=t.get('titulo', ''),
                descricao=t.get('descricao', ''),
                estado=t.get('estado', ''),
                data_criacao=t.get('data_criacao', t.get('data_criacao', '')),
                data_limite=t.get('data_limite', t.get('data_limite', ''))
            )
            tarefas.append(tarefa)
        return tarefas


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

        try:
            validar_com_xsd(nova)
        except Exception as e:
            return f"Tarefa inválida: {str(e)}"

        tarefas = carregar_tarefas()
        tarefas.append(nova)
        guardar_tarefas(tarefas)

        return "Tarefa criada com sucesso"

# --- Configuração do servidor ---

app = Application([TarefaService],
                  tns='soap.tarefas',
                  in_protocol=Soap11(),
                  out_protocol=Soap11())

wsgi_app = WsgiApplication(app)

if __name__ == '__main__':
    from wsgiref.simple_server import make_server
    print("SOAP service a correr em http://0.0.0.0:8002")
    make_server('0.0.0.0', 8002, wsgi_app).serve_forever()
