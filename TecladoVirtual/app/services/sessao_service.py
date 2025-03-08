import random
import uuid
from flask import jsonify, request
from app import current_app as app

def criar_sessao():
    # Gerar uma sequência aleatória
    numeros = list(range(10))
    random.shuffle(numeros)

    # Gerar um ID único para a sessão
    sessao_id = str(uuid.uuid4())

    # Preparar os dados da sessão para inserção no banco
    dados_sessao = {"_id": sessao_id, "sequencia": numeros}

    # Inserir no banco de dados MongoDB
    colecao = app.db["sessoes"]
    colecao.insert_one(dados_sessao)

    # Retornar o ID da sessão e a sequência
    return jsonify({"sessao_id": sessao_id, "sequencia": numeros})

def validar_sequencia():
    dados = request.json
    sessao_id = dados.get("sessao_id")
    sequencia_usuario = dados.get("sequencia")

    colecao = app.db["sessoes"]

    # Verificar se a sessão existe no banco
    sessao = colecao.find_one({"_id": sessao_id})

    if not sessao:
        return jsonify({"sucesso": False, "mensagem": "Sessão inválida ou expirada!"}), 400

    # Validar a sequência fornecida pelo usuário
    if sequencia_usuario == sessao["sequencia"]:
        colecao.delete_one({"_id": sessao_id})
        return jsonify({"sucesso": True, "mensagem": "Sequência correta!"})

    return jsonify({"sucesso": False, "mensagem": "Sequência incorreta!"}), 400
