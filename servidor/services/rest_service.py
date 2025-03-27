from flask import Flask, request, jsonify
import json
import os

app = Flask(__name__)
data_file = "data/chat_data.json"

def load_data():
    if os.path.exists(data_file):
        with open(data_file, "r", encoding="utf-8") as f:
            return json.load(f)
    return {"groups": {}}

def save_data(data):
    with open(data_file, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)

@app.route("/groups", methods=["POST"])
def create_group():
    data = load_data()
    group_name = request.json.get("group_name")
    if group_name in data["groups"]:
        return jsonify({"error": "Grupo já existe!"}), 400
    data["groups"][group_name] = {"messages": []}
    save_data(data)
    return jsonify({"message": "Grupo criado com sucesso!"})

@app.route("/groups/<group_name>/messages", methods=["POST"])
def send_message(group_name):
    data = load_data()
    if group_name not in data["groups"]:
        return jsonify({"error": "Grupo não encontrado!"}), 404
    message = request.json.get("message")
    data["groups"][group_name]["messages"].append(message)
    save_data(data)
    return jsonify({"message": "Mensagem enviada!"})

@app.route("/groups/<group_name>/messages", methods=["GET"])
def get_messages(group_name):
    data = load_data()
    if group_name not in data["groups"]:
        return jsonify({"error": "Grupo não encontrado!"}), 404
    return jsonify(data["groups"][group_name]["messages"])
