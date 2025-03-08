from pymongo import MongoClient
import os

# Carrega a URI do MongoDB do ambiente
MONGO_URI = os.getenv("MONGO_URI", "mongodb+srv://nahuelayala055:<dD1nwtvwq3EaBcK3a>@cluster0.luw32.mongodb.net/")

# Inicializa o MongoDB
client = MongoClient(MONGO_URI)
db = client["meu_banco"]  # Nome do banco de dados

def get_db():
    """Retorna a instância do banco de dados"""
    return db
