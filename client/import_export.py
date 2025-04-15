import requests

def exportar(formato):
    if formato == 'json':
        return requests.get('http://127.0.0.1:5000/export/json').json()
    elif formato == 'xml':
        return requests.get('http://127.0.0.1:5000/export/xml').text

def importar_json():
    dados = [{"titulo": "Importada", "descricao": "Via JSON", "estado": "pendente", "data_limite": "2025-04-30"}]
    return requests.post('http://127.0.0.1:5000/import/json', json=dados).json()

def importar_xml():
    xml = '''<tarefas><tarefa><titulo>Importada</titulo><descricao>Via XML</descricao><estado>pendente</estado><data_limite>2025-04-30</data_limite></tarefa></tarefas>'''
    headers = {'Content-Type': 'application/xml'}
    return requests.post('http://127.0.0.1:5000/import/xml', data=xml, headers=headers).json()
