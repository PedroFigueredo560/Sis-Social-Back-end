from database import db

class Beneficiario(db.Model):
    name_ben = db.Column(db.String(50), nullable = False)
    cpf = db.Column(db.String(14), nullable = False, primary_key = True)
    services = db.Column(db.String(50), nullable = False)
    user_ben = db.Column(db.String(50), nullable = False)
    password_ben = db.Column(db.String(50), nullable = False)
    
    def __init__(self, name, cpf, services, user, password):
        self.name_func = name
        self.cpf = cpf
        self.services = services
        self.user_func = user
        self.password_func = password
        
    def to_dictionary(self):
        return{
            'name_func': self.name_func,
            'cpf': self.cpf,
            'services': self.services,
            'user_func': self.user_func,
            'password_func': self.password_func
        }