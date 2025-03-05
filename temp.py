from flask import Flask, request, jsonify
import redis
import uuid
import json

app = Flask(__name__)

# Conectar ao Redis
redis_client = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)

# Tempo de expiração da sessão (em segundos)
SESSION_TIMEOUT = 300  

@app.route("/criar_sessao", methods=["POST"])
def criar_sessao():
    """Cria uma nova sessão temporária com sequência aleatória"""
    numeros = list(range(10))  # Exemplo de números 0-9
    import random
    random.shuffle(numeros)  # Embaralha os números

    sessao_id = str(uuid.uuid4())  # Gera um ID único para a sessão
    dados_sessao = {"sequencia": numeros}

    # Salva no Redis com tempo de expiração
    redis_client.setex(sessao_id, SESSION_TIMEOUT, json.dumps(dados_sessao))

    return jsonify({"sessao_id": sessao_id, "sequencia": numeros})


@app.route("/validar", methods=["POST"])
def validar_sequencia():
    """Valida a sequência enviada pelo usuário"""
    dados = request.json
    
    # Verifica se os dados estão no formato correto
    if not dados or "sessao_id" not in dados or "sequencia" not in dados:
        return jsonify({"sucesso": False, "mensagem": "Dados incompletos ou inválidos!"}), 400
    
    sessao_id = dados.get("sessao_id")
    sequencia_usuario = dados.get("sequencia")

    # Recupera a sessão do Redis
    sessao = redis_client.get(sessao_id)
    
    if not sessao:
        return jsonify({"sucesso": False, "mensagem": "Sessão inválida ou expirada!"}), 400

    sessao = json.loads(sessao)  # Converte de JSON para dicionário
    if sequencia_usuario == sessao["sequencia"]:
        # Se a sequência for correta, remove a sessão e aprova
        redis_client.delete(sessao_id)
        return jsonify({"sucesso": True, "mensagem": "Sequência correta!"})
    
    return jsonify({"sucesso": False, "mensagem": "Sequência incorreta!"}), 400


if __name__ == "__main__":
    app.run(debug=True)
