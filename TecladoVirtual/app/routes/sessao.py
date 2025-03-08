from flask import Blueprint, jsonify, request
from app.services.sessao_service import criar_sessao, validar_sequencia

# Criar a blueprint para as rotas relacionadas a sessões
sessao_bp = Blueprint('sessao', __name__)

@sessao_bp.route("/criar_sessao", methods=["POST"])
def criar():
    return criar_sessao()

@sessao_bp.route("/validar", methods=["POST"])
def validar():
    return validar_sequencia()
