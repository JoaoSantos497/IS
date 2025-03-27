from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import json
import os

DATA_FILE = "data/data.json"

app = FastAPI()

class User(BaseModel):
    id: int
    name: str

# Carregar dados do arquivo JSON
def load_data():
    if not os.path.exists(DATA_FILE):
        return []
    with open(DATA_FILE, "r") as file:
        return json.load(file)

# Salvar dados no arquivo JSON
def save_data(data):
    with open(DATA_FILE, "w") as file:
        json.dump(data, file, indent=4)

@app.get("/users")
def get_users():
    return load_data()

@app.post("/users")
def create_user(user: User):
    data = load_data()
    if any(u["id"] == user.id for u in data):
        raise HTTPException(status_code=400, detail="ID já existe")
    data.append(user.dict())
    save_data(data)
    return user

@app.get("/users/{user_id}")
def get_user(user_id: int):
    data = load_data()
    user = next((u for u in data if u["id"] == user_id), None)
    if not user:
        raise HTTPException(status_code=404, detail="Utilizador não encontrado")
    return user

@app.delete("/users/{user_id}")
def delete_user(user_id: int):
    data = load_data()
    data = [u for u in data if u["id"] != user_id]
    save_data(data)
    return {"message": "Utilizador deletado"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8002)
