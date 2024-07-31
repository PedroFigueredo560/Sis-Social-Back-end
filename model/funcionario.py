from database import db
class Funcionario(db.Model):
    __tablename__ = 'funcionario'
    
    name_func = db.Column(db.String(50), nullable=False)
    cpf = db.Column(db.String(14), nullable=False, primary_key=True)
    job = db.Column(db.String(50), nullable=False)
    user_func = db.Column(db.String(50), nullable=False)
    password_func = db.Column(db.String(50), nullable=False)

    def __init__(self, name_func, cpf, job, user_func, password_func):
        self.name_func = name_func
        self.cpf = cpf
        self.job = job
        self.user_func = user_func
        self.password_func = password_func
        
    def to_dictionary(self):
        return {
            'name_func': self.name_func,
            'cpf': self.cpf,
            'job': self.job,
            'user_func': self.user_func,
            'password_func': self.password_func
        }