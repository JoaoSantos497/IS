import requests

def graphql_query(url, group_name):
    query = """
    query {
        hello(name: "Grupo1")
    }
    """
    response = requests.post(url, json={'query': query})
    if response.status_code == 200:
        return response.json()
    else:
        print("Erro ao fazer consulta GraphQL")
        return None
