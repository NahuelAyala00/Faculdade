import pytest
from temp import app  # Importe a instância do Flask 'app' do arquivo 'temp.py'

@pytest.fixture
def client():
    with app.test_client() as client:
        yield client  # Isso cria o client para os testes

def test_criar_sessao(client):
    response = client.post('/criar_sessao')
    assert response.status_code == 200
    assert 'sessao_id' in response.json
    assert 'sequencia' in response.json

def test_validar_sequencia(client):
    response = client.post('/criar_sessao')
    sessao_id = response.json['sessao_id']
    sequencia = response.json['sequencia']
    
    # Enviar a sequência correta
    response = client.post('/validar', json={'sessao_id': sessao_id, 'sequencia': sequencia})
    assert response.status_code == 200
    assert response.json['sucesso'] is True
    
    # Enviar a sequência errada
    response = client.post('/validar', json={'sessao_id': sessao_id, 'sequencia': [1, 2, 3, 4, 5, 6, 7, 8, 9, 0]})
    assert response.status_code == 400
    assert response.json['sucesso'] is False
