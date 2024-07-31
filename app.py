"""
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
def create_finac():
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
"""




# CONEXÃO FUNCIONANDO COM O FRONT-END

from flask import Flask, request, jsonify
from flask_cors import CORS
from database import app, db
from model.beneficiario import Beneficiario
from model.agendamento import Agendamento
from model.horarios_disponiveis import DisponibilidadeHorarios
from datetime import datetime, timezone, timedelta
from model.auth_decorator import token_required
from functools import wraps
import pytz
import jwt
from model.funcionario import Funcionario
from model.financeiro import Financa
from marshmallow import Schema, fields, ValidationError  

# Configuração do CORS
CORS(app)

app.config['SECRET_KEY'] = '0098766754'

@app.route('/create_ben', methods=['POST'])
def create_ben():
    data = request.json
    try:
        new_beneficiario = Beneficiario(
            name_ben=data.get('name_ben'),
            cpf=data.get('cpf'),
            services=data.get('services'),
            user_ben=data.get('user_ben'),
            password_ben=data.get('password_ben')
        )
        db.session.add(new_beneficiario)
        db.session.commit()
        return jsonify({'message': 'Beneficiário criado com sucesso'}), 201
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({'error': str(e)}), 400
@app.route('/validate_login_ben', methods=['POST'])
def validate_login_ben():
    data = request.get_json()
    user = data.get('user')
    password = data.get('password')

    ben = Beneficiario.query.filter_by(user_ben=user, password_ben=password).first()

    if ben:
        # Gera um token JWT
        token = jwt.encode({'user': ben.user_ben}, app.config['SECRET_KEY'], algorithm='HS256')
        return jsonify({'message': 'Logado com sucesso', 'token': token})
    else:
        return jsonify({'message': 'Usuário não encontrado'}), 401
@app.route('/check_cpf/<string:cpf>', methods=['GET'])
def check_cpf(cpf):
    try:
        beneficiario = Beneficiario.query.filter_by(cpf=cpf).first()
        if beneficiario:
            return jsonify({'message': 'CPF encontrado'}), 200
        else:
            return jsonify({'message': 'CPF não encontrado'}), 404
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({'error': str(e)}), 400
    
@app.route('/get_func', methods = ['GET'])
def get_func():
    try:
        funcs = Agendamento.query.all()
        return jsonify([func.to_dictionary() for func in funcs]), 200
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({'error': str(e)}), 400

@app.route('/create_agendamento', methods=['POST'])
@token_required
def create_agendamento():
    data = request.get_json()
    try:
        beneficiario = Beneficiario.query.filter_by(cpf=data['cpf']).first()
        if not beneficiario:
            return jsonify({'error': 'CPF não encontrado na base de dados'}), 400

        agendamento_data = datetime.fromisoformat(data['data']).astimezone(timezone.utc)
        print(f"Agendamento data recebida: {agendamento_data}")

        # Verifica se já existe um agendamento para a mesma data e hora
        existing_appointment = Agendamento.query.filter_by(data=agendamento_data).first()
        if existing_appointment:
            return jsonify({"error": "Já existe um agendamento para esta data e hora."}), 400

        new_agendamento = Agendamento(
            cpf=data['cpf'],
            nome=data['nome'],
            telefone=data['telefone'],
            data=agendamento_data,
            descricao=data['descricao'],
            status=data['status'],
            observacoes=data.get('observacoes'),
            email_notification=data.get('email_notification', False)
        )
        db.session.add(new_agendamento)
        db.session.commit()
        return jsonify(new_agendamento.to_dictionary()), 201
    except Exception as e:
        db.session.rollback()
        print(f"Error: {e}")
        return jsonify({'error': str(e)}), 400

@app.route('/agendamentos', methods=['GET'])
def get_agendamentos():
    try:
        agendamentos = Agendamento.query.all()
        return jsonify([a.to_dictionary() for a in agendamentos]), 200
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({'error': str(e)}), 400

@app.route('/agendamento/<int:id>', methods=['GET'])
def get_agendamento(id):
    try:
        agendamento = Agendamento.query.get(id)
        if not agendamento:
            return jsonify({'error': 'Agendamento não encontrado'}), 404
        return jsonify(agendamento.to_dictionary()), 200
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({'error': str(e)}), 400

@app.route('/agendamento/<int:id>', methods=['PUT'])
def update_agendamento(id):
    data = request.get_json()
    try:
        agendamento = Agendamento.query.get(id)
        if not agendamento:
            return jsonify({'error': 'Agendamento não encontrado'}), 404

        agendamento.cpf = data.get('cpf', agendamento.cpf)
        agendamento.nome = data.get('nome', agendamento.nome)
        agendamento.telefone = data.get('telefone', agendamento.telefone)
        agendamento.data = datetime.fromisoformat(data.get('data', agendamento.data.isoformat()))
        agendamento.descricao = data.get('descricao', agendamento.descricao)
        agendamento.status = data.get('status', agendamento.status)
        agendamento.observacoes = data.get('observacoes', agendamento.observacoes)
        
        db.session.commit()
        return jsonify(agendamento.to_dictionary()), 200
    except Exception as e:
        db.session.rollback()
        print(f"Error: {e}")
        return jsonify({'error': str(e)}), 400

@app.route('/agendamento/<int:id>', methods=['DELETE'])
def delete_agendamento(id):
    try:
        agendamento = Agendamento.query.get(id)
        if not agendamento:
            return jsonify({'error': 'Agendamento não encontrado'}), 404
        db.session.delete(agendamento)
        db.session.commit()
        return jsonify({'message': 'Agendamento deletado com sucesso'}), 200
    except Exception as e:
        db.session.rollback()
        print(f"Error: {e}")
        return jsonify({'error': str(e)}), 400
@app.route('/available_slots', methods=['GET'])
def available_slots():
    date_str = request.args.get('date')
    if not date_str:
        return jsonify({"error": "Data não fornecida"}), 400
    try:
        date = datetime.strptime(date_str, '%Y-%m-%d').date()
        
        existing_agendamentos = Agendamento.query.filter(
            Agendamento.data.between(
                datetime.combine(date, datetime.min.time()),
                datetime.combine(date, datetime.max.time())
            ),
            Agendamento.status != 'cancelado'
        ).all()

        slots = []
        start_times = ['08:00', '14:00']
        end_times = ['11:00', '17:00']
        duration = timedelta(minutes=50)
        
        for start_time, end_time in zip(start_times, end_times):
            start = datetime.combine(date, datetime.strptime(start_time, '%H:%M').time())
            end = datetime.combine(date, datetime.strptime(end_time, '%H:%M').time())
            
            while start + duration <= end:
                slot_end = start + duration
                slot = start.strftime('%H:%M') + '-' + slot_end.strftime('%H:%M')
                
                slot_start = start
                slot_end = slot_end
                is_occupied = any(
                    agendamento.data <= slot_end and
                    agendamento.data + timedelta(minutes=50) > slot_start
                    for agendamento in existing_agendamentos
                )
                
                if not is_occupied:
                    slots.append(slot)
                
                start = slot_end

        return jsonify({'slots': slots})
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({'error': str(e)}), 400


@app.route('/create_finac', methods=['POST'])
def create_finac():
    data = request.json
    try:
        new_Financa = Financa(
            descricao=data.get('descricao'),
            valor=data.get('valor'),
            categoria=data.get('categoria'),
            data_reg=data.get('data_reg'),
        )
        db.session.add(new_Financa)
        db.session.commit()
        return jsonify({'message': 'Transação registrada com sucesso'}), 201
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({'error': str(e)}), 400
    
@app.route('/delete_finac', methods=['DELETE'])
def delete_finac():
  finac = Financa.query.get(request.json.get('id'))
  if finac is None:
    return jsonify({'error': 'Financial already deleted or not found!'}), 404
  
  db.session.delete(finac)
  db.session.commit()
  
  return jsonify({'message': 'Financial deleted successfully!'}), 200
    
@app.route('/get_finac', methods=['GET'])
def get_finac():
    # Fetch all Financa objects using query.all()
    financas = Financa.query.all()

    finac_data = [
    {'id': finac.id, 'data_reg': finac.data_reg, 'descricao': finac.descricao, 'categoria': finac.categoria, 'valor': finac.valor}
    for finac in financas
]
    # Return the JSON-formatted data
    return jsonify(finac_data)

@app.route('/update_finac/<int:id>', methods=['PUT'])
def update_finac(id):
  data = request.get_json()
  financa = Financa.query.get(id)
  if financa is None:
    return jsonify({'error': 'Transação não encontrada'}), 404

  financa.descricao = data.get('descricao', financa.descricao)
  financa.valor = data.get('valor', financa.valor)
  financa.categoria = data.get('categoria',financa.categoria)
  # Atualize outros campos conforme necessário

  db.session.commit()
  return jsonify({'message': 'Transação atualizada com sucesso'}), 200
    

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(port=5000, debug=True)
    
    