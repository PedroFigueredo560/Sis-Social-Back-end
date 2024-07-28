from database import db

class DisponibilidadeHorarios(db.Model):
    __tablename__ = 'disponibilidade_horarios'
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.DateTime(timezone=True), nullable=False)  
    horario = db.Column(db.String, nullable=False)

    def __init__(self, data, horario):
        self.data = data
        self.horario = horario

    def __repr__(self):
        return f"<DisponibilidadeHorarios(data={self.data}, horario={self.horario})>"
