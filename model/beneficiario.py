from database import db

class Beneficiario(db.Model):
    __tablename__ = 'beneficiario'
    
    name_ben = db.Column(db.String(50), nullable=False)
    cpf = db.Column(db.String(11), nullable=False, primary_key=True)
    services = db.Column(db.String(50), nullable=False)
    user_ben = db.Column(db.String(50), nullable=False)
    password_ben = db.Column(db.String(50), nullable=False)
    
    def __init__(self, name_ben, cpf, services, user_ben, password_ben):
        self.name_ben = name_ben
        self.cpf = cpf
        self.services = services
        self.user_ben = user_ben
        self.password_ben = password_ben
        
    def to_dictionary(self):
        return {
            'name_ben': self.name_ben,
            'cpf': self.cpf,
            'services': self.services,
            'user_ben': self.user_ben,
            'password_ben': self.password_ben
        }




# CODIFO FUNCIONANDO
# from database import db

# class Beneficiario(db.Model):
#     __tablename__ = 'beneficiario'
    
#     name_ben = db.Column(db.String(50), nullable=False)
#     cpf = db.Column(db.String(11), nullable=False, primary_key=True)
#     services = db.Column(db.String(50), nullable=False)
#     user_ben = db.Column(db.String(50), nullable=False)
#     password_ben = db.Column(db.String(50), nullable=False)
    
#     def __init__(self, name_ben, cpf, services, user_ben, password_ben):
#         self.name_ben = name_ben
#         self.cpf = cpf
#         self.services = services
#         self.user_ben = user_ben
#         self.password_ben = password_ben
        
#     def to_dictionary(self):
#         return {
#             'name_ben': self.name_ben,
#             'cpf': self.cpf,
#             'services': self.services,
#             'user_ben': self.user_ben,
#             'password_ben': self.password_ben
#         }
