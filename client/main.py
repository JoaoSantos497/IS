from flask import Flask, render_template, request, redirect, jsonify, Response
import rest_client
import soap_client
import graphql_client
import grpc_client
import dicttoxml


app = Flask(__name__)

# Página inicial
@app.route('/')
def index():
    return render_template('index.html')

# Rotas para APIs
@app.route('/rest')
def rest():
    return redirect('/tarefas/rest')  # Redireciona para a rota de listar tarefas REST

@app.route('/soap')
def soap():
    return redirect('/tarefas/soap')  # Redireciona para a rota de listar tarefas SOAP

@app.route('/graphql')
def graphql():
    return redirect('/tarefas/graphql')  # Redireciona para a rota de listar tarefas GraphQL

@app.route('/grpc')
def grpc():
    return redirect('/tarefas/grpc')  # Redireciona para a rota de listar tarefas gRPC

# API para listar tarefas de diferentes serviços
@app.route('/tarefas/<servico>', methods=['GET'])
def listar_tarefas(servico):
    tarefas = []
    try:
        if servico == 'rest':
            tarefas = rest_client.listar_tarefas()
        elif servico == 'soap':
            print("SOAP não implementado")
            tarefas = soap_client.listar_tarefas()
        elif servico == 'graphql':
            tarefas = graphql_client.listar_tarefas()
        elif servico == 'grpc':
            tarefas = grpc_client.listar_tarefas()
    except Exception as e:
        tarefas = []
        print(f"Erro ao listar tarefas via {servico}: {e}")
    print(tarefas)
    return render_template('listar_tarefas.html', tarefas=tarefas, servico=servico)

# API REST para criar uma nova tarefa
@app.route('/tarefas/rest', methods=['POST'])
def criar_tarefa_rest():
    try:
        dados = request.get_json()
        rest_client.criar_tarefa(**dados)
        return jsonify({"message": "Tarefa criada com sucesso!"}), 201
    except Exception as e:
        return jsonify({"error": f"Erro ao criar tarefa: {e}"}), 400

# API REST para atualizar uma tarefa existente
@app.route('/tarefas/rest/<int:id>', methods=['PUT'])
def atualizar_tarefa_rest(id):
    try:
        dados = request.get_json()
        rest_client.atualizar_tarefa(id, **dados)
        return jsonify({"message": "Tarefa atualizada com sucesso!"})
    except Exception as e:
        return jsonify({"error": f"Erro ao atualizar tarefa: {e}"}), 400

# API REST para deletar uma tarefa
@app.route('/tarefas/rest/<int:id>', methods=['DELETE'])
def deletar_tarefa_rest(id):
    try:
        rest_client.deletar_tarefa(id)
        return jsonify({"message": "Tarefa deletada com sucesso!"})
    except Exception as e:
        return jsonify({"error": f"Erro ao deletar tarefa: {e}"}), 400

# API SOAP
@app.route('/soap', methods=['POST'])
def soap_api():
    try:
        dados = request.data  # A requisição SOAP usa XML
        resposta = soap_client.processar_requisicao(dados)  # Supondo que existe essa função
        return resposta, 200
    except Exception as e:
        return jsonify({"error": f"Erro ao processar requisição SOAP: {e}"}), 400

# API GraphQL
@app.route('/graphql', methods=['POST'])
def graphql_api():
    try:
        query = request.get_json().get("query")  # A requisição GraphQL envia uma consulta
        resposta = graphql_client.executar_query(query)
        return jsonify(resposta), 200
    except Exception as e:
        return jsonify({"error": f"Erro ao executar consulta GraphQL: {e}"}), 400

# API gRPC
@app.route('/grpc', methods=['POST'])
def grpc_api():
    try:
        dados = request.get_json()
        resposta = grpc_client.executar_servico(dados)
        return jsonify(resposta), 200
    except Exception as e:
        return jsonify({"error": f"Erro ao processar requisição gRPC: {e}"}), 400
    
@app.route('/tarefas/<servico>/export/json', methods=['GET'])
def export_tarefas_json(servico):
    tarefas = []
    try:
        if servico == 'rest':
            tarefas = rest_client.listar_tarefas()
        elif servico == 'soap':
            print("SOAP não implementado")
            tarefas = soap_client.listar_tarefas()
        elif servico == 'graphql':
            tarefas = graphql_client.listar_tarefas()
        elif servico == 'grpc':
            tarefas = grpc_client.listar_tarefas()
    except Exception as e:
        tarefas = []
        print(f"Erro ao listar tarefas via {servico}: {e}")
    print(tarefas)
    return jsonify(tarefas)

@app.route('/tarefas/<servico>/export/xml', methods=['GET'])
def export_tarefas_xml(servico):
    tarefas = []
    try:
        if servico == 'rest':
            tarefas = rest_client.listar_tarefas()
        elif servico == 'soap':
            print("SOAP não implementado")
            tarefas = soap_client.listar_tarefas()
        elif servico == 'graphql':
            tarefas = graphql_client.listar_tarefas()
        elif servico == 'grpc':
            tarefas = grpc_client.listar_tarefas()
        else:
            raise ValueError(f"Serviço {servico} não suportado.")
        
        # Verifica se as tarefas são uma lista
        if not isinstance(tarefas, list):
            tarefas = []  # Se não for, torna tarefas uma lista vazia
    except Exception as e:
        tarefas = []
        print(f"Erro ao listar tarefas via {servico}: {e}")
    
    # Converter lista de tarefas para XML
    xml_data = dicttoxml.dicttoxml(tarefas, custom_root='tarefas', ids=False)
    
    # Retornar a resposta em XML com o tipo de conteúdo correto
    return Response(xml_data, mimetype='application/xml')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
