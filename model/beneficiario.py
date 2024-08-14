from sqlalchemy import DateTime
from database import db

class Beneficiario(db.Model):
    __tablename__ = 'beneficiario'
    
    name_ben = db.Column(db.String(50), nullable=False)
    cpf = db.Column(db.String(11), nullable=False, primary_key=True)
    nascimento = db.Column(DateTime, nullable=False)
    telefone = db.Column(db.String(16))
    endereco = db.Column(db.String(50))
    servicos = db.Column(db.String(50), nullable=False)
    user_ben = db.Column(db.String(50), nullable=False)
    password_ben = db.Column(db.String(50), nullable=False)
    
    def __init__(self, name_ben, cpf, nascimento, telefone, endereco, servicos, user_ben, password_ben):
        self.name_ben = name_ben
        self.cpf = cpf
        self.nascimento = nascimento
        self.telefone = telefone
        self.endereco = endereco
        self.servicos = servicos
        self.user_ben = user_ben
        self.password_ben = password_ben
        
    def to_dictionary(self):
        return {
            'name_ben': self.name_ben,
            'cpf': self.cpf,
            'nascimento': self.nascimento,
            'telefone': self.telefone,
            'endereco': self.endereco,
            'servicos': self.servicos,
            'user_ben': self.user_ben,
            'password_ben': self.password_ben
        }