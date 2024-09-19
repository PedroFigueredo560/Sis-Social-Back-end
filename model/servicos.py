from sqlalchemy import Column, Integer
from database import db

class Servicos(db.Model):
    __tablename__ = 'servicos'
    
    nome_servicos = Column(db.String(50), nullable=False, primary_key=True)
    criterios = Column(db.String(50), nullable=False)
    horario = Column(db.String(8))
    data = Column(db.String(10))
    locais = Column(db.String(50))

    def __init__(self, name, criterios, horario, data, locais):
        self.nome_servicos = name
        self.criterios = criterios
        self.horario = horario
        self.data = data
        self.locais = locais

    def to_dictionary(self):
        return {
            'nome_servicos': self.nome_servicos,
            'criterios': self.criterios,
            'horario': self.horario,
            'data': self.data,
            'locais': self.locais
        }
