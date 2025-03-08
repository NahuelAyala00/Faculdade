class Sessao:
    def __init__(self, sessao_id, sequencia):
        self.sessao_id = sessao_id
        self.sequencia = sequencia

    def to_dict(self):
        """Converte o objeto para um dicionário"""
        return {"_id": self.sessao_id, "sequencia": self.sequencia}
