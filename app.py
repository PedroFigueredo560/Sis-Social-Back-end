from flask import Flask, jsonify, request
from database import app, db
from model.funcionario import Funcionario



#Isso não passa de um main que pode ser alterado
#e pode ser usado como um exemplo de como funciona
#uma função em flask, LEIA O TXT CHAMADO 'LEIA_ISSO.txt'

#initialise flask api
#app = Flask(__name__)

#configure database
#app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://your_username:your_password@localhost/sis_social'
#app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

#db = Database(app)

@app.route('/create_func', methods = ['POST'])
def create_func():
    if request.method == 'POST':
        name = request.json['name_func']
        cpf = request.json['cpf']
        job = request.json['job']
        user = request.json['user_func']
        password = request.json['password_func']
        
        new_func = Funcionario(name, cpf, job, user, password)
        db.session.add(new_func)
        db.session.commit
        return jsonify(new_func.to_dictionary())
    
@app.route('/get_func', methods = ['GET'])
def get_func():
    funcs = Funcionario.query.all
    return jsonify([{'nome_func': func.name_func, 'cpf': func.cpf, 'job': func.job}for func in funcs])

@app.route('/get_user_func', methods = ['GET'])
def get_user_func():
    cpf = request.json.get('cpf')
    
    func = Funcionario.query.filter_by(cpf=cpf).first()
    
    if func:
        return jsonify({'username': func.user_func, 'password': func.user_password})
    else:
        return jsonify({'error': 'User not found!'})
    
@app.route('/delete_func', methods = ['DELETE'])
def delete_func():
    func = Funcionario.query.get(request.json.get('cpf'))
    if func is None:
        return jsonify({'error': 'User already deleted or not found!'})
    
    db.session.delete(func)
    db.session.commit()
    
    return jsonify({'message': 'User deleted successfully!'})

@app.route('/update_func', methods = ['PUT'])
def update_func():
    func = Funcionario.query.get(request.json.get('cpf'))
    
    if func is None:
        return jsonify({'error': 'User not found!'})
    
    data = request.json
    if 'name_func' in data:
        func.name_func = data['name_func']
    if 'cpf' in data:
        func.cpf = data['cpf']
    if 'job' in data:
        func.job = data['job']
    if 'user_func' in data:
        func.user_func = data['user_func']
    if 'password_func' in data:
        func.password_func = data['password_func']
        
    db.session.commit()
    
    return jsonify({'message': 'User successfully updated!'})

@app.route('/')
def hello_world():
    return 'Hello World'

if __name__ == '__main__':
    app.run(debug=True)
