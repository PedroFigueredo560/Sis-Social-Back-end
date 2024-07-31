from database import db
from sqlalchemy import Column, Integer, String, DateTime

class Financa(db.Model):
    __tablename__ = 'financa'

    id = Column(Integer, primary_key=True,autoincrement=True)
    data_reg = Column(DateTime, nullable=False) 
    descricao = Column(String(500), nullable=False)
    categoria = Column(String(50), nullable=False)
    valor = Column(db.Float, nullable=False)

    def __init__(self, data_reg, descricao, categoria, valor):
        self.data_reg = data_reg
        self.descricao = descricao
        self.categoria = categoria
        self.valor = valor

    def to_dictionary(self):
        formatted_date = self.data_reg.strftime('%d/%m/%Y')  # Assuming desired date format

        return {
            'id': self.id,
            'data_reg': formatted_date,
            'descricao': self.descricao,
            'categoria': self.categoria,
            'valor': self.valor
        }