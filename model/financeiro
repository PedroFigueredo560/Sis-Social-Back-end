from database import db

class Financa(db.Model):
    id = db.Column(db.Float,nullable=False,primary_key=True)  
    data_reg = db.Column(db.String(50), nullable=False)
    descricao = db.Column(db.String(500), nullable=False)
    categoria = db.Column(db.String(50), nullable=False)
    valor = db.Column(db.Float, nullable=False)

    def __init__(self, id,data_reg, descricao, categoria, valor):
        self.id = id 
        self.data_reg = data_reg
        self.descricao = descricao
        self.categoria = categoria
        self.valor = valor

    def to_dictionary(self):
        return {
            'id': self.id,
            'data_reg': self.data_reg,
            'descricao': self.descricao,
            'categoria': self.categoria,
            'valor': self.valor
        }