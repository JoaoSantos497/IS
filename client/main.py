from flask import Flask, render_template, request, redirect
import rest_client
import soap_client
import graphql_client
import grpc_client
import import_export

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/tarefas/<servico>')
def listar_tarefas(servico):
    if servico == 'rest':
        tarefas = rest_client.listar_tarefas()
    elif servico == 'soap':
        tarefas = soap_client.listar_tarefas()
    elif servico == 'graphql':
        tarefas = graphql_client.listar_tarefas()
    elif servico == 'grpc':
        tarefas = grpc_client.listar_tarefas()
    else:
        tarefas = []
    return render_template('tarefas.html', tarefas=tarefas, servico=servico)

@app.route('/tarefas/<servico>/criar', methods=['GET', 'POST'])
def criar_tarefa(servico):
    if request.method == 'POST':
        dados = {
            "titulo": request.form['titulo'],
            "descricao": request.form['descricao'],
            "estado": request.form['estado'],
            "data_limite": request.form['data_limite']
        }
        if servico == 'rest':
            rest_client.criar_tarefa(**dados)
        elif servico == 'soap':
            soap_client.criar_tarefa(**dados)
        elif servico == 'graphql':
            graphql_client.criar_tarefa(**dados)
        elif servico == 'grpc':
            grpc_client.criar_tarefa(**dados)
        return redirect(f'/tarefas/{servico}')
    return render_template('criar_tarefa.html', servico=servico)

@app.route('/exportar/<formato>')
def exportar(formato):
    dados = import_export.exportar(formato)
    return f"<pre>{dados}</pre>"

@app.route('/importar/<formato>', methods=['GET', 'POST'])
def importar(formato):
    if request.method == 'POST':
        if formato == 'json':
            import_export.importar_json()
        elif formato == 'xml':
            import_export.importar_xml()
        return redirect('/')
    return f'<form method="post"><button type="submit">Importar {formato.upper()}</button></form>'

if __name__ == '__main__':
    app.run(debug=True)
