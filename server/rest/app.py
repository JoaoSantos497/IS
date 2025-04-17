from flask import Flask, jsonify, request
from jsonschema import validate, ValidationError
import os
import json
import uuid
import xmltodict
from datetime import datetime

app = Flask(__name__)
base_dir = os.path.dirname(os.path.abspath(__file__))
SCHEMA_PATH = os.path.join(base_dir, 'schema', 'tarefa.schema.json')
DADOS_JSON = os.path.join(base_dir, '../dados/tarefas.json')

# Load JSON Schema
with open(SCHEMA_PATH) as f:
    schema = json.load(f)

def carregar_tarefas():
    if os.path.exists(DADOS_JSON):
        with open(DADOS_JSON) as f:
            return json.load(f)
    return []

def guardar_tarefas(tarefas):
    with open(DADOS_JSON, 'w') as f:
        json.dump(tarefas, f, indent=2)

@app.route('/tarefas', methods=['GET'])
def listar():
    return jsonify(carregar_tarefas())

@app.route('/tarefas', methods=['POST'])
def criar():
    nova = request.json
    try:
        nova['id'] = str(uuid.uuid4())
        nova['data_criacao'] = datetime.now().strftime('%Y-%m-%d')
        validate(instance=nova, schema=schema)
        tarefas = carregar_tarefas()
        tarefas.append(nova)
        guardar_tarefas(tarefas)
        return jsonify(nova), 201
    except ValidationError as e:
        return jsonify({'erro': str(e)}), 400

@app.route('/tarefas/<id>', methods=['PUT'])
def atualizar(id):
    atualizada = request.json
    try:
        atualizada['id'] = id
        validate(instance=atualizada, schema=schema)
        tarefas = carregar_tarefas()
        for i, t in enumerate(tarefas):
            if t['id'] == id:
                tarefas[i] = atualizada
                guardar_tarefas(tarefas)
                return jsonify(atualizada)
        return jsonify({'erro': 'Tarefa não encontrada'}), 404
    except ValidationError as e:
        return jsonify({'erro': str(e)}), 400

@app.route('/tarefas/<id>', methods=['DELETE'])
def apagar(id):
    tarefas = carregar_tarefas()
    tarefas_novas = [t for t in tarefas if t['id'] != id]
    if len(tarefas) == len(tarefas_novas):
        return jsonify({'erro': 'Tarefa não encontrada'}), 404
    guardar_tarefas(tarefas_novas)
    return '', 204

@app.route('/export/json', methods=['GET'])
def exportar_json():
    return jsonify(carregar_tarefas())

@app.route('/import/json', methods=['POST'])
def importar_json():
    dados = request.json
    if isinstance(dados, list):
        try:
            for d in dados:
                validate(instance=d, schema=schema)
            guardar_tarefas(dados)
            return jsonify({'mensagem': 'Importado com sucesso'})
        except ValidationError as e:
            return jsonify({'erro': str(e)}), 400
    return jsonify({'erro': 'Formato inválido'}), 400

@app.route('/export/xml', methods=['GET'])
def exportar_xml():
    tarefas = carregar_tarefas()
    xml = xmltodict.unparse({'tarefas': {'tarefa': tarefas}}, pretty=True)
    return app.response_class(xml, mimetype='application/xml')

@app.route('/import/xml', methods=['POST'])
def importar_xml():
    try:
        xml = request.data
        obj = xmltodict.parse(xml)
        tarefas = obj['tarefas']['tarefa']
        if isinstance(tarefas, dict):
            tarefas = [tarefas]
        for t in tarefas:
            validate(instance=t, schema=schema)
        guardar_tarefas(tarefas)
        return jsonify({'mensagem': 'Importado com sucesso'})
    except Exception as e:
        return jsonify({'erro': str(e)}), 400

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8001)
