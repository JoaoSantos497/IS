import graphene
from flask import Flask, request, jsonify
import uuid
from datetime import datetime
from jsonschema import validate, ValidationError
import json
import os

base_dir = os.path.dirname(os.path.abspath(__file__))
SCHEMA_PATH = os.path.join(base_dir, 'schema', 'tarefa.schema.json')
DADOS_JSON = os.path.join(base_dir, '../dados/tarefas.json')


# Carregar JSON Schema
with open(SCHEMA_PATH) as f:
    tarefa_schema = json.load(f)

def carregar_tarefas():
    if os.path.exists(DADOS_JSON):
        with open(DADOS_JSON) as f:
            return json.load(f)
    return []

def guardar_tarefas(tarefas):
    with open(DADOS_JSON, 'w') as f:
        json.dump(tarefas, f, indent=2)

class Tarefa(graphene.ObjectType):
        
    id = graphene.String()
    titulo = graphene.String()
    descricao = graphene.String()
    estado = graphene.String()
    data_criacao = graphene.String()  # Corrigido para camelCase
    data_limite = graphene.String()   # Corrigido para camelCase

class CriarTarefa(graphene.Mutation):
    class Arguments:
        titulo = graphene.String(required=True)
        descricao = graphene.String(required=True)
        estado = graphene.String(required=True)
        data_limite = graphene.String(required=True)  # Corrigido para camelCase
        data_criacao = graphene.String()  # Corrigido para camelCase

    tarefa = graphene.Field(Tarefa)

    def mutate(self, info, titulo, descricao, estado, data_limite, data_criacao=None):
        nova_tarefa = {
            "id": str(uuid.uuid4()),
            "titulo": titulo,
            "descricao": descricao,
            "estado": estado,
            "data_criacao": datetime.now().strftime("%Y-%m-%d"),  # Corrigido para camelCase
            "data_limite": data_limite  # Corrigido para camelCase
        }

        try:
            validate(instance=nova_tarefa, schema=tarefa_schema)
        except ValidationError as e:
            raise Exception(f"Tarefa inválida: {e.message}")

        tarefas = carregar_tarefas()
        tarefas.append(nova_tarefa)
        guardar_tarefas(tarefas)

        return CriarTarefa(tarefa=nova_tarefa)

class Query(graphene.ObjectType):
    tarefas = graphene.List(Tarefa)

    def resolve_tarefas(self, info):
        return carregar_tarefas()

class Mutation(graphene.ObjectType):
    criar_tarefa = CriarTarefa.Field()

app = Flask(__name__)
schema = graphene.Schema(query=Query, mutation=Mutation)

@app.route('/graphql', methods=['POST'])
def graphql_server():
    data = request.get_json()
    result = schema.execute(data.get('query'), variables=data.get('variables'))
    
    response = {}
    if result.errors:
        response['errors'] = [str(e) for e in result.errors]
    if result.data:
        response['data'] = result.data
    
    return jsonify(response)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8003)
