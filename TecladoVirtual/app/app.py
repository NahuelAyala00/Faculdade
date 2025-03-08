import os
from flask import Flask
from dotenv import load_dotenv
from pymongo import MongoClient
from app.routes import sessao_bp

# Carregar variáveis de ambiente
load_dotenv()

def create_app():
    app = Flask(__name__)

    # Configurações do banco de dados MongoDB
    app.config["MONGO_URI"] = os.getenv("MONGO_URI", "mongodb+srv://<user>:<password>@cluster0.luw32.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
    
    # Configuração do MongoDB
    client = MongoClient(app.config["MONGO_URI"])
    db = client["meu_banco"]
    app.db = db  # Passando o db para a aplicação

    # Registra a blueprint de sessões
    app.register_blueprint(sessao_bp, url_prefix='/sessao')

    return app
