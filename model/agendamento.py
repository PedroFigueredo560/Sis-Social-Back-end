from database import db
from datetime import datetime

class Agendamento(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    cpf = db.Column(db.String(11), db.ForeignKey('beneficiario.cpf'), nullable=False)
    nome = db.Column(db.String(100), nullable=False)
    telefone = db.Column(db.String(15), nullable=False)
    data = db.Column(db.DateTime, nullable=False)
    descricao = db.Column(db.String(255), nullable=False)
    status = db.Column(db.String(50), nullable=False)
    observacoes = db.Column(db.Text, nullable=True)

    def __init__(self, cpf, nome, telefone, data, descricao, status, observacoes=None):
        self.cpf = cpf
        self.nome = nome
        self.telefone = telefone
        self.data = data
        self.descricao = descricao
        self.status = status
        self.observacoes = observacoes

    def to_dictionary(self):
        return {
            'id': self.id,
            'cpf': self.cpf,
            'nome': self.nome,
            'telefone': self.telefone,
            'data': self.data.isoformat(),
            'descricao': self.descricao,
            'status': self.status,
            'observacoes': self.observacoes
        }
