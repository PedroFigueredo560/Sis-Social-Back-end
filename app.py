from flask import Flask, jsonify, request
from database import app, db
from model.beneficiario import Beneficiario
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
        return jsonify({'user_func': func.user_func, 'password_func': func.user_password})
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

@app.route('/create_ben', methods = ['POST'])
def create_ben():
    if request.method == 'POST':
        name = request.json['name_ben']
        cpf = request.json['cpf']
        user = request.json['user_ben']
        password = request.json['password_ben']
        
        new_ben = Beneficiario(name, cpf, user, password)
        db.session.add(new_ben)
        db.session.commit
        return jsonify(new_ben.to_dictionary())
    
@app.route('/get_ben', methods = ['GET'])
def get_ben():
    bens = Beneficiario.query.all
    return jsonify([{'nome_ben': ben.name_func, 'cpf': ben.cpf, 'services': ben.services}for ben in bens])

@app.route('/get_user_ben', methods = ['GET'])
def get_user_ben():
    cpf = request.json.get('cpf')
    
    ben = Beneficiario.query.filter_by(cpf=cpf).first()
    
    if ben:
        return jsonify({'user_ben': ben.user_ben, 'password_ben': ben.user_password})
    else:
        return jsonify({'error': 'User not found!'})
    
@app.route('/delete_ben', methods = ['DELETE'])
def delete_ben():
    ben = Beneficiario.query.get(request.json.get('cpf'))
    if ben is None:
        return jsonify({'error': 'User already deleted or not found!'})
    
    db.session.delete(ben)
    db.session.commit()

@app.route('/update_ben', methods = ['PUT'])
def update_ben():
    ben = Beneficiario.query.get(request.json.get('cpf'))
    
    if ben is None:
        return jsonify({'error': 'User not found!'})
    
    data = request.json
    if 'name_ben' in data:
        ben.name_func = data['name_ben']
    if 'cpf' in data:
        ben.cpf = data['cpf']
    if 'job' in data:
        ben.job = data['job']
    if 'user_ben' in data:
        ben.user_func = data['user_ben']
    if 'password_func' in data:
        ben.password_ben = data['password_ben']
        
    db.session.commit()
    
    return jsonify({'message': 'User successfully updated!'})

@app.route('/')
def hello_world():
    return 'Hello World'

if __name__ == '__main__':
    app.run(debug=True)
