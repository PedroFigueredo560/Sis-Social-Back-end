from database import db

class Servicos(db.Model):
    nome_servicos = db.Column(db.String(50), nullable=False)  # Use snake_case for variable names
    criterios = db.Column(db.String(50), nullable=False)  # Consistent capitalization
    horario = db.Column(db.String(8), nullable=False, primary_key=True)
    data = db.Column(db.String(10), nullable=False)
    locais = db.Column(db.String(50), nullable=False)

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
