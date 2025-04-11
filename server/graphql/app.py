from flask import Flask, request, jsonify
import graphene
import json
import os
import uuid
from datetime import datetime
from jsonschema import validate, ValidationError

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SCHEMA_PATH = os.path.join(BASE_DIR, 'schema', 'tarefa.schema.json')
DADOS_JSON = os.path.join(BASE_DIR, 'dados.json')  # Adicione isso se quiser persistência

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

# GraphQL Types
class Tarefa(graphene.ObjectType):
    id = graphene.String()
    titulo = graphene.String()
    descricao = graphene.String()
    estado = graphene.String()
    data_criacao = graphene.String()
    data_limite = graphene.String()

class Query(graphene.ObjectType):
    tarefas = graphene.List(Tarefa)

    def resolve_tarefas(self, info):
        return carregar_tarefas()

class CriarTarefa(graphene.Mutation):
    class Arguments:
        titulo = graphene.String(required=True)
        descricao = graphene.String(required=True)
        estado = graphene.String(required=True)
        data_limite = graphene.String(required=True)

    tarefa = graphene.Field(lambda: Tarefa)

    def mutate(self, info, titulo, descricao, estado, data_limite):
        nova = {
            "id": str(uuid.uuid4()),
            "titulo": titulo,
            "descricao": descricao,
            "estado": estado,
            "data_criacao": datetime.now().strftime("%Y-%m-%d"),
            "data_limite": data_limite
        }
        try:
            validate(instance=nova, schema=tarefa_schema)
        except ValidationError as e:
            raise Exception(f"Tarefa inválida: {e.message}")

        tarefas = carregar_tarefas()
        tarefas.append(nova)
        guardar_tarefas(tarefas)
        return CriarTarefa(tarefa=nova)

class Mutation(graphene.ObjectType):
    criar_tarefa = CriarTarefa.Field()

# App
app = Flask(__name__)
schema = graphene.Schema(query=Query, mutation=Mutation)

@app.route('/graphql', methods=['POST'])
def graphql_server():
    data = request.get_json()
    result = schema.execute(data.get('query'), variables=data.get('variables'))
    return jsonify(result.data)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=4000)
