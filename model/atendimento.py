from datetime import datetime, timedelta, timezone
from apscheduler.schedulers.background import BackgroundScheduler
from database import db

class Atendimento(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    cpfFunc = db.Column(db.String(11), db.ForeignKey('funcionario.cpf'), nullable=False)
    cpfBen = db.Column(db.String(11), db.ForeignKey('beneficiario.cpf'), nullable=False)
    assunto = db.Column(db.String(1000), nullable=False)
    data = db.Column(db.DateTime(timezone=True), nullable=False)
    duracao = db.Column(db.Integer)

    def __init__(self, cpfFunc, cpfBen, assunto, data, duracao):
        # Verifique se o parâmetro 'data' é uma string e, em seguida, converta-o em datetime
        if isinstance(data, str):
            data = datetime.fromisoformat(data)
        self.cpfFunc = cpfFunc
        self.cpfBen = cpfBen
        self.assunto = assunto
        self.data = data.astimezone(timezone.utc)
        self.duracao = duracao

    def to_dictionary(self):
        return {
            'id': self.id,
            'cpfFunc': self.cpfFunc,
            'cpfBen': self.cpfBen,
            'assunto': self.assunto,
            'data': self.data.isoformat(),
            'duracao': self.duracao,
        }