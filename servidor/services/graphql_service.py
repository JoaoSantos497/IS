from flask import Flask
from graphene import ObjectType, String, Schema
from flask_graphql import GraphQLView

app = Flask(__name__)

class Query(ObjectType):
    hello = String(name=String(default_value="stranger"))

    def resolve_hello(self, info, name):
        return f"Olá, {name}!"

schema = Schema(query=Query)

def start_graphql_server():
    app.add_url_rule('/graphql', view_func=GraphQLView.as_view('graphql', schema=schema, graphiql=True))
    app.run(port=5002)
