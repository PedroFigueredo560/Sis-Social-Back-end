from datetime import datetime, timedelta, timezone
from apscheduler.schedulers.background import BackgroundScheduler
# from .email_utils import send_email
from database import db

class Agendamento(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    cpf = db.Column(db.String(11), db.ForeignKey('beneficiario.cpf'), nullable=False)
    nome = db.Column(db.String(100), nullable=False)
    telefone = db.Column(db.String(15), nullable=False)
    data = db.Column(db.DateTime(timezone=True), nullable=False)
    descricao = db.Column(db.String(255), nullable=False)
    status = db.Column(db.String(50), nullable=False)
    observacoes = db.Column(db.Text, nullable=True)
    email_notification = db.Column(db.Boolean, default=False)
    email = db.Column(db.String(255), nullable=True)  

    def __init__(self, cpf, nome, telefone, data, descricao, status, observacoes=None, email_notification=False, email=None):
        self.cpf = cpf
        self.nome = nome
        self.telefone = telefone
        self.data = data.astimezone(timezone.utc)
        self.descricao = descricao
        self.status = status
        self.observacoes = observacoes
        self.email_notification = email_notification
        self.email = email  # Adiciona o e-mail

    def to_dictionary(self):
        return {
            'id': self.id,
            'cpf': self.cpf,
            'nome': self.nome,
            'telefone': self.telefone,
            'data': self.data.isoformat(),
            'descricao': self.descricao,
            'status': self.status,
            'observacoes': self.observacoes,
            'email_notification': self.email_notification,
            'email': self.email  
        }

# def send_notifications():
#     try:
#         now = datetime.utcnow()
#         notification_time = now + timedelta(days=1)

#         # Buscar agendamentos que estão programados para amanhã
#         agendamentos = Agendamento.query.filter(
#             Agendamento.data.between(
#                 notification_time.replace(hour=0, minute=0, second=0, microsecond=0),
#                 notification_time.replace(hour=23, minute=59, second=59, microsecond=999999)
#             ),
#             Agendamento.email_notification == True
#         ).all()

#         for agendamento in agendamentos:
#             subject = "Lembrete de Agendamento"
#             body = f"Olá {agendamento.nome},\n\nEste é um lembrete de que você tem um agendamento marcado para amanhã, {agendamento.data}.\n\nAtenciosamente,\nSua Empresa"
#             print(f"Enviando e-mail para {agendamento.email}")
#             send_email(agendamento.email, subject, body)

#     except Exception as e:
#         print(f"Error: {e}")
