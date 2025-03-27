from fastapi import FastAPI
from starlette.graphql import GraphQLApp
import json
import os
from graphene import ObjectType, String, Int, List, Field, Schema

DATA_FILE = "data/data.json"

# Carregar dados do arquivo JSON
def load_data():
    if not os.path.exists(DATA_FILE):
        return []
    with open(DATA_FILE, "r") as file:
        return json.load(file)

# Modelo GraphQL
class UserType(ObjectType):
    id = Int()
    name = String()

# Query GraphQL
class Query(ObjectType):
    users = List(UserType)

    def resolve_users(root, info):
        return load_data()

# Mutations GraphQL
class CreateUser(ObjectType):
    class Arguments:
        id = Int()
        name = String()

    user = Field(UserType)

    def mutate(self, info, id, name):
        data = load_data()
        if any(u["id"] == id for u in data):
            raise Exception("ID já existe")
        new_user = {"id": id, "name": name}
        data.append(new_user)
        with open(DATA_FILE, "w") as file:
            json.dump(data, file, indent=4)
        return CreateUser(user=new_user)

class Mutation(ObjectType):
    create_user = CreateUser.Field()

schema = Schema(query=Query, mutation=Mutation)

app = FastAPI()
app.add_route("/graphql", GraphQLApp(schema=schema))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8003)
