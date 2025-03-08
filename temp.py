from flask import Flask, request, jsonify
from pymongo import MongoClient
import uuid
import random

app = Flask(__name__)

# Conectar ao MongoDB (localmente ou no Atlas)
client = MongoClient("mongodb+srv://nahuelayala055:D1nwtvwq3EaBcK3a@cluster0.luw32.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")  # Altere para o seu MongoDB se necessário
db = client["meu_banco"]  # Criar/usar o banco
colecao = db["sessoes"]  # Criar/usar a coleção

@app.route("/criar_sessao", methods=["POST"])
def criar_sessao():
    """Cria uma nova sessão no MongoDB"""
    numeros = list(range(10))
    random.shuffle(numeros)

    sessao_id = str(uuid.uuid4())
    dados_sessao = {"_id": sessao_id, "sequencia": numeros}

    # Salvar no MongoDB
    colecao.insert_one(dados_sessao)

    return jsonify({"sessao_id": sessao_id, "sequencia": numeros})

@app.route("/validar", methods=["POST"])
def validar_sequencia():
    """Valida a sequência enviada pelo usuário"""
    dados = request.json
    sessao_id = dados.get("sessao_id")
    sequencia_usuario = dados.get("sequencia")

    # Buscar sessão no MongoDB
    sessao = colecao.find_one({"_id": sessao_id})

    if not sessao:
        return jsonify({"sucesso": False, "mensagem": "Sessão inválida ou expirada!"}), 400

    if sequencia_usuario == sessao["sequencia"]:
        colecao.delete_one({"_id": sessao_id})  # Remover após validação
        return jsonify({"sucesso": True, "mensagem": "Sequência correta!"})
    
    return jsonify({"sucesso": False, "mensagem": "Sequência incorreta!"}), 400

if __name__ == "__main__":
    app.run(debug=True)