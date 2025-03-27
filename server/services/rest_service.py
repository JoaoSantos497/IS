from flask import Flask, request, jsonify
import json
import os
import xmltodict

app = Flask(__name__)
data_file = "data/chat_data.json"
xml_file = "data/chat_data.xml"

# Função para carregar os dados do arquivo JSON
def load_data():
    if os.path.exists(data_file):
        with open(data_file, "r", encoding="utf-8") as f:
            return json.load(f)
    return {"groups": {}}

# Função para salvar os dados no arquivo JSON
def save_data(data):
    with open(data_file, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)

# Função para exportar dados para JSON
def export_data_to_json():
    data = load_data()
    with open(data_file, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)
    return "Dados exportados para JSON com sucesso!"

# Função para importar dados de JSON
def import_data_from_json():
    if os.path.exists(data_file):
        with open(data_file, "r", encoding="utf-8") as f:
            data = json.load(f)
        save_data(data)
        return "Dados importados de JSON com sucesso!"
    return "Arquivo JSON não encontrado."

# Função para exportar dados para XML
def export_data_to_xml():
    data = load_data()
    with open(xml_file, "w", encoding="utf-8") as f:
        xml_data = json_to_xml(data)
        f.write(xml_data)
    return "Dados exportados para XML com sucesso!"

# Função para importar dados de XML
def import_data_from_xml():
    if os.path.exists(xml_file):
        with open(xml_file, "r", encoding="utf-8") as f:
            xml_data = f.read()
        data = xml_to_json(xml_data)
        save_data(data)
        return "Dados importados de XML com sucesso!"
    return "Arquivo XML não encontrado."

# Função para converter JSON para XML
def json_to_xml(data):
    return xmltodict.unparse(data, pretty=True)

# Função para converter XML para JSON
def xml_to_json(xml_data):
    return xmltodict.parse(xml_data)

# Rota para criar grupos
@app.route("/groups", methods=["POST"])
def create_group():
    data = load_data()
    group_name = request.json.get("group_name")
    if group_name in data["groups"]:
        return jsonify({"error": "Grupo já existe!"}), 400
    data["groups"][group_name] = {"messages": []}
    save_data(data)
    return jsonify({"message": "Grupo criado com sucesso!"})

# Rota para enviar mensagens
@app.route("/groups/<group_name>/messages", methods=["POST"])
def send_message(group_name):
    data = load_data()
    if group_name not in data["groups"]:
        return jsonify({"error": "Grupo não encontrado!"}), 404
    message = request.json.get("message")
    data["groups"][group_name]["messages"].append(message)
    save_data(data)
    return jsonify({"message": "Mensagem enviada!"})

# Rota para obter mensagens
@app.route("/groups/<group_name>/messages", methods=["GET"])
def get_messages(group_name):
    data = load_data()
    if group_name not in data["groups"]:
        return jsonify({"error": "Grupo não encontrado!"}), 404
    return jsonify(data["groups"][group_name]["messages"])

# Rota para exportar dados para JSON
@app.route("/export/json", methods=["GET"])
def export_json():
    result = export_data_to_json()
    return jsonify({"message": result})

# Rota para importar dados de JSON
@app.route("/import/json", methods=["POST"])
def import_json():
    result = import_data_from_json()
    return jsonify({"message": result})

# Rota para exportar dados para XML
@app.route("/export/xml", methods=["GET"])
def export_xml():
    result = export_data_to_xml()
    return jsonify({"message": result})

# Rota para importar dados de XML
@app.route("/import/xml", methods=["POST"])
def import_xml():
    result = import_data_from_xml()
    return jsonify({"message": result})

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
