import os
from app.app import create_app
from pymongo import MongoClient
from flask import jsonify
import pytest
import sys
import os

# Adiciona o diretório raiz ao sys.path para localizar o módulo 'app'
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.app import create_app  # Agora deve funcionar

# Resto do código de teste...


# Configuração para recuperar a URI do MongoDB de variáveis de ambiente
MONGO_URI = os.getenv('MONGO_URI', 'mongodb+srv://nahuelayala055:<dD1nwtvwq3EaBcK3a>@cluster0.luw32.mongodb.net/')  # Exemplo de URI

@pytest.fixture
def client():
    # Criação do app para testes
    app = create_app()
    app.config['TESTING'] = True
    app.config['MONGO_URI'] = MONGO_URI  # Banco de dados de teste
    with app.test_client() as client:
        yield client

@pytest.fixture(scope="function", autouse=True)
def cleanup_db():
    # Conectar ao banco de dados de teste e limpar a coleção antes de cada teste
    mongo_client = MongoClient(MONGO_URI)
    db = mongo_client["meu_banco_test"]
    db.sessoes.delete_many({})  # Limpa a coleção após cada teste

def test_criar_sessao(client):
    # Testa a criação da sessão
    response = client.post('/criar_sessao')
    assert response.status_code == 200
    json_data = response.get_json()
    assert 'sessao_id' in json_data
    assert 'sequencia' in json_data
    assert len(json_data['sequencia']) == 10  # A sequência deve ter 10 números

    # Verificar se a sessão foi criada no banco de dados
    mongo_client = MongoClient(MONGO_URI)
    db = mongo_client["meu_banco_test"]
    sessao = db.sessoes.find_one({"_id": json_data["sessao_id"]})
    assert sessao is not None
    assert "sequencia" in sessao

def test_validar_sequencia_correta(client):
    # Testa a validação da sequência correta
    response = client.post('/criar_sessao')
    sessao_id = response.get_json()['sessao_id']
    sequencia = response.get_json()['sequencia']

    response = client.post('/validar', json={'sessao_id': sessao_id, 'sequencia': sequencia})
    assert response.status_code == 200
    assert response.get_json()['sucesso'] is True
    assert response.get_json()['mensagem'] == "Sequência correta!"

def test_validar_sequencia_incorreta(client):
    # Testa a validação da sequência incorreta
    response = client.post('/criar_sessao')
    sessao_id = response.get_json()['sessao_id']
    sequencia_errada = [1, 2, 3, 4, 5, 6, 7, 8, 9, 0]

    response = client.post('/validar', json={'sessao_id': sessao_id, 'sequencia': sequencia_errada})
    assert response.status_code == 400
    assert response.get_json()['sucesso'] is False
    assert response.get_json()['mensagem'] == "Sequência incorreta!"

def test_validar_sessao_inexistente(client):
    # Testa a validação de uma sessão inexistente
    sessao_id_inexistente = "nonexistent_id"
    sequencia_errada = [1, 2, 3, 4, 5, 6, 7, 8, 9, 0]

    response = client.post('/validar', json={'sessao_id': sessao_id_inexistente, 'sequencia': sequencia_errada})
    assert response.status_code == 400
    assert response.get_json()['sucesso'] is False
    assert response.get_json()['mensagem'] == "Sessão inválida ou expirada!"
