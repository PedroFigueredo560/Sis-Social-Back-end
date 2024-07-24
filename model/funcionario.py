from database import db

class Funcionario(db.Model):
    name_func = db.Column(db.String(50), nullable = False)
    cpf = db.Column(db.String(14), nullable = False, primary_key = True)
    job = db.Column(db.String(50), nullable = False)
    user_func = db.Column(db.String(50), nullable = False)
    password_func = db.Column(db.String(50), nullable = False)
    
    def __init__(self, name, cpf, job, user, password):
        self.name_func = name
        self.cpf = cpf
        self.job = job
        self.user_func = user
        self.password_func = password
        
    def to_dictionary(self):
        return{
            'name_func': self.name_func,
            'cpf': self.cpf,
            'job': self.job,
            'user_func': self.user_func,
            'password_func': self.password_func
        }