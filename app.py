from flask import Flask, jsonify, request
from database import app, db
from model.beneficiario import Beneficiario
from model.funcionario import Funcionario
from model.financeiro import Financa


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
    data=request.get_json()()
    
    name = data.get('name_func')
    cpf = data.get('cpf')
    job = data.get('job')
    user = data.get('user_func')
    password = data.get('password_func')
    
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
    data=request.get_json()
    
    name = data.get('name_ben')
    cpf = data.get('cpf')
    user = data.get('user_ben')
    password = data.get('password_ben')
    
    new_ben = Beneficiario(name, cpf, 'solicitante', user, password)
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

@app.route('/create_finac', methods = ['POST'])
def create_func():
    data=request.get_json()()
    id = data.get('id')
    data_reg = data.get('data_reg')
    descricao = data.get('descricao')
    categoria = data.get('categoria')
    valor = data.get('valor')
    
    new_finac = Financa(id, data_reg, descricao, categoria, valor)
    db.session.add(new_finac)
    db.session.commit
    return jsonify(new_finac.to_dictionary())

@app.route('/get_finac', methods = ['GET'])
def get_finac():
    finac = Financa.query.all
    return jsonify([{'id': finac.id}for finac in finac])
    
@app.route('/delete_finac', methods = ['DELETE'])
def delete_finac():
    finac = Financa.query.get(request.json.get('id'))
    if finac is None:
        return jsonify({'error': 'Financial already deleted or not found!'})
    
    db.session.delete(finac)
    db.session.commit()
    
    return jsonify({'message': 'Finacial deleted successfully!'})

@app.route('/update_finac', methods = ['PUT'])
def update_finac():
    finac = Financa.query.get(request.json.get('id'))
    
    if finac is None:
        return jsonify({'error': 'Finacial not found!'})
    
    data = request.json
    if 'id' in data:
        finac.name_func = data['id']
    if 'data_reg' in data:
        finac.data_reg = data['data_reg']
    if 'descricao' in data:
        finac.descricao = data['descricao']
    if 'categoria' in data:
        finac.categoria = data['categoria']
    if 'valor' in data:
        finac.valor = data['valor']
        
    db.session.commit()
    
    return jsonify({'message': 'Financial successfully updated!'})
@app.route('/')
def hello_world():
    return 'Hello World'

with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)
