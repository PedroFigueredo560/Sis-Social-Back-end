from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from flask_mail import Mail, Message
from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime, timezone, timedelta
from database import app, db
from model.beneficiario import Beneficiario
from model.agendamento import Agendamento
from model.atendimento import Atendimento
from model.horarios_disponiveis import DisponibilidadeHorarios
from model.auth_decorator import token_required
from functools import wraps
import pytz
import jwt
from model.funcionario import Funcionario
from model.financeiro import Financa
from marshmallow import Schema, fields, ValidationError  
from model.servicos import Servicos
from werkzeug.utils import secure_filename
import os
from flask_socketio import SocketIO, send, emit, join_room, leave_room

# Configuração do CORS
CORS(app)

app.config['SECRET_KEY'] = '0098766754'

# Configuração do Flask-Mail
smtp_server = "smtp.gmail.com"
smtp_port = 587
app.config['MAIL_USERNAME'] = 'usuarioEmail'
app.config['MAIL_PASSWORD'] = 'senha'
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False

mail = Mail(app)
scheduler = BackgroundScheduler()
scheduler.start()

def send_email(to, subject, body):
    msg = Message(subject, sender='usuarioEmail', recipients=[to])
    msg.body = body
    mail.send(msg)

@app.route('/create_ben', methods=['POST'])
def create_ben():
    data = request.get_json()
    try:
        new_beneficiario = Beneficiario(
            name_ben=data.get('name_ben'),
            cpf=data.get('cpf'),
            nascimento=data.get('nascimento'),
            telefone=data.get('telefone'),
            endereco=data.get('endereco'),
            servicos=data.get('servicos'),
            user_ben=data.get('user_ben'),
            password_ben=data.get('password_ben')
        )
        db.session.add(new_beneficiario)
        db.session.commit()
        return jsonify({'message': 'Beneficiário criado com sucesso'}), 201
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({'error': str(e)}), 400
    
@app.route('/get_ben', methods = ['GET'])
def get_ben():
    try:
        bens = Beneficiario.query.all()
        return jsonify([ben.to_dictionary() for ben in bens]), 200
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({'error': str(e)}), 400
    
@app.route('/get_beneficiario/<cpf>', methods = ['GET'])
def get_user_ben(cpf):    
    ben = Beneficiario.query.filter_by(cpf=cpf).first()
    
    if ben:
        return jsonify({'nome_ben': ben.name_ben, 'cpf': ben.cpf, 'nascimento': ben.nascimento, 'telefone': ben.telefone, 'endereco': ben.endereco, 'servicos': ben.servicos,'user_ben': ben.user_ben, 'password_ben': ben.password_ben})
    else:
        return jsonify({'error': 'User not found!'})
    
@app.route('/update_beneficiario', methods=['PUT'])
def update_beneficiario():
    data = request.get_json()
    try:
        beneficiario = Beneficiario.query.get(data.get('cpf'))
        if not beneficiario:
            return jsonify({'error': 'Beneficiário não encontrado'}), 404

        beneficiario.cpf = data.get('cpf', beneficiario.cpf)
        beneficiario.name_ben = data.get('nome_ben', beneficiario.name_ben)
        beneficiario.telefone = data.get('telefone', beneficiario.telefone)
        beneficiario.endereco = data.get('endereco', beneficiario.endereco)
        beneficiario.servicos = data.get('servicos', beneficiario.servicos)
        beneficiario.user_ben = data.get('user_ben', beneficiario.user_ben)
        beneficiario.password_ben = data.get('password_ben', beneficiario.password_ben)
        
        db.session.commit()
        return jsonify({'message': 'Editado com sucesso'}), 200
    except Exception as e:
        db.session.rollback()
        print(f"Error: {e}")
        return jsonify({'error': str(e)}), 400
    
@app.route('/delete_beneficiario', methods=['DELETE'])
def delete_beneficiario():
    data = request.get_json()
    try:
        beneficiario = Beneficiario.query.get(data)
        if not beneficiario:
            return jsonify({'error': 'Beneficiário não encontrado'}), 404
        db.session.delete(beneficiario)
        db.session.commit()
        return jsonify({'message': 'Beneficiário deletado com sucesso'}), 200
    except Exception as e:
        db.session.rollback()
        print(f"Error: {e}")
        return jsonify({'error': str(e)}), 400

@app.route('/validate_login', methods=['POST'])
def validate_login():
    data = request.get_json()
    user = data.get('user')
    password = data.get('password')

    ben = Beneficiario.query.filter_by(user_ben=user, password_ben=password).first()
    if ben:
        token = jwt.encode({
            'user': ben.user_ben,
            'role': 'beneficiario'
        }, app.config['SECRET_KEY'], algorithm='HS256')
        return jsonify({'message': 'Logado como beneficiário', 'token': token})

    func = Funcionario.query.filter_by(user_func=user, password_func=password).first()
    if func:
        token = jwt.encode({
            'user': func.user_func,
            'role': 'funcionario'
        }, app.config['SECRET_KEY'], algorithm='HS256')
        return jsonify({'message': 'Logado como funcionário', 'token': token})

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
    
@app.route('/create_func', methods=['POST'])
def create_func():
    data = request.get_json()
    try:
        print(f"Received data: {data}")
        new_funcionario = Funcionario(
            name_func=data.get('name_func'),
            cpf=data.get('cpf'),
            job=data.get('job'),
            user_func=data.get('user_func'),
            password_func=data.get('password_func')
        )
        db.session.add(new_funcionario)
        db.session.commit()
        return jsonify({'message': 'Funcionario criado com sucesso'}), 201
    except Exception as e:
        db.session.rollback()
        print(f"Error: {e}")
        return jsonify({'error': str(e)}), 400
    
@app.route('/get_func', methods = ['GET'])
def get_func():
    try:
        funcs = Funcionario.query.all()
        return jsonify([func.to_dictionary() for func in funcs]), 200
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({'error': str(e)}), 400
    
@app.route('/get_funcionario/<cpf>', methods = ['GET'])
def get_user_func(cpf):    
    func = Funcionario.query.filter_by(cpf=cpf).first()
    
    if func:
        return jsonify({'nome_func': func.name_func, 'cpf': func.cpf, 'job': func.job,'user_func': func.user_func, 'password_func': func.password_func})
    else:
        return jsonify({'error': 'User not found!'})

@app.route('/update_funcionario', methods=['PUT'])
def update_funcionario():
    data = request.get_json()
    try:
        funcionario = Funcionario.query.get(data.get('cpf'))
        if not funcionario:
            return jsonify({'error': 'Funcionario não encontrado'}), 404

        # Atualize apenas os campos fornecidos
        funcionario.name_func = data.get('name_func', funcionario.name_func)
        funcionario.job = data.get('job', funcionario.job)
        funcionario.user_func = data.get('user_func', funcionario.user_func)
        funcionario.password_func = data.get('password_func', funcionario.password_func)
        
        db.session.commit()
        return jsonify({'message': 'Funcionario editado com sucesso'}), 200
    except Exception as e:
        db.session.rollback()
        print(f"Error: {e}")
        return jsonify({'error': str(e)}), 400
    
@app.route('/delete_funcionario', methods=['DELETE'])
def delete_funcionario():
    data = request.get_json()
    try:
        funcionario = Funcionario.query.get(data)
        if not funcionario:
            return jsonify({'error': 'Funcionário não encontrado'}), 404
        db.session.delete(funcionario)
        db.session.commit()
        return jsonify({'message': 'Funcionário deletado com sucesso'}), 200
    except Exception as e:
        db.session.rollback()
        print(f"Error: {e}")
        return jsonify({'error': str(e)}), 400
    
@app.route('/create_servicos', methods=['POST'])
def create_servicos():
    data = request.get_json()
    try:
        new_servicos = Servicos(
            nome_servicos=data.get('nome_servicos'),
            criterios=data.get('criterios'),
            horario=data.get('horario'),
            data=data.get('data'),
            locais=data.get('locais')
        )
        db.session.add(new_servicos)
        db.session.commit()
        return jsonify({'message': 'Serviço criado com sucesso'}), 201
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({'error': str(e)}), 400
    
@app.route('/get_servicos', methods = ['GET'])
def get_servicos():
    try:
        servs = Servicos.query.all()
        return jsonify([serv.to_dictionary() for serv in servs]), 200
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({'error': str(e)}), 400
    
@app.route('/get_servico/<servico_name>', methods=['GET'])
def get_servico(servico_name):

    servico = Servicos.query.filter_by(nome_servicos=servico_name).first()

    if servico:
        return jsonify({
            'nome_servicos': servico.nome_servicos,
            'criterios': servico.criterios,
            'horario': servico.horario,
            'data': servico.data,
            'locais': servico.locais
        })
    else:
        return jsonify({'error': 'Service not found!'}), 404

@app.route('/update_servico', methods=['PUT'])
def update_servico():
    data = request.get_json()
    try:
        serv = Servicos.query.get(data.get('nome_servicos'))
        if not serv:
            return jsonify({'error': 'Serviço não encontrado'}), 404

        serv.nome_servicos = data.get('nome_servicos', serv.nome_servicos)
        serv.criterios = data.get('criterios', serv.criterios)
        serv.horario = data.get('horario', serv.horario)
        serv.data = data.get('data', serv.data)
        serv.locais = data.get('locais', serv.locais)
        
        db.session.commit()
        return jsonify({'message': 'Editado com sucesso'}), 200
    except Exception as e:
        db.session.rollback()
        print(f"Error: {e}")
        return jsonify({'error': str(e)}), 400
    
@app.route('/delete_servico', methods=['DELETE'])
def delete_servico():
    data = request.get_json()
    try:
        serv = Servicos.query.get(data)
        if not serv:
            return jsonify({'error': 'Serviço não encontrado'}), 404
        db.session.delete(serv)
        db.session.commit()
        return jsonify({'message': 'Serviço deletado com sucesso'}), 200
    except Exception as e:
        db.session.rollback()
        print(f"Error: {e}")
        return jsonify({'error': str(e)}), 400

@app.route('/create_agendamento', methods=['POST'])
@token_required
def create_agendamento():
    data = request.get_json()
    print(f"Dados recebidos para agendamento: {data}")

    try:
        if 'cpf' not in data or 'data' not in data or 'nome' not in data or 'telefone' not in data or 'descricao' not in data or 'status' not in data:
            print("Dados insuficientes recebidos.")
            return jsonify({'error': 'Dados insuficientes para criar agendamento'}), 400

        # Verificar se o beneficiário existe
        beneficiario = Beneficiario.query.filter_by(cpf=data['cpf']).first()
        if not beneficiario:
            print(f"Beneficiário com CPF {data['cpf']} não encontrado.")
            return jsonify({'error': 'CPF não encontrado na base de dados'}), 400

        # Converter e verificar a data do agendamento
        try:
            agendamento_data = datetime.fromisoformat(data['data']).astimezone(timezone.utc)
            print(f"Data do agendamento convertida: {agendamento_data}")
        except ValueError as ve:
            print(f"Erro ao converter a data do agendamento: {ve}")
            return jsonify({'error': 'Data inválida'}), 400

        # Verificar se já existe um agendamento para a mesma data e hora
        existing_appointment = Agendamento.query.filter_by(data=agendamento_data).first()
        if existing_appointment:
            print(f"Já existe um agendamento para a data e hora: {agendamento_data}")
            return jsonify({"error": "Já existe um agendamento para esta data e hora."}), 400

        # Criar o novo agendamento
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
        print(f"Novo agendamento criado: {new_agendamento.to_dictionary()}")

        # Enviar email de confirmação
        # if new_agendamento.email_notification:
        #     print(f"Enviando email de confirmação para: {beneficiario.user_ben}")
        #     send_email(
        #         to=beneficiario.user_ben,
        #         subject="Confirmação de Agendamento",
        #         body=f"Seu agendamento está confirmado para {new_agendamento.data}."
        #     )

        #     # Agendar o envio do alerta um dia antes
        #     alert_time = new_agendamento.data - timedelta(days=1)
        #     print(f"Agendando alerta para: {alert_time}")
        #     scheduler.add_job(
        #         send_email,
        #         'date',
        #         run_date=alert_time,
        #         args=[beneficiario.user_ben, "Lembrete de Agendamento", f"Seu agendamento é amanhã às {new_agendamento.data}."]
        #     )

        return jsonify(new_agendamento.to_dictionary()), 201
    except Exception as e:
        db.session.rollback()
        print(f"Erro ao criar agendamento: {e}")
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
    

# Configurando a pasta de upload
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)  # Cria a pasta se não existir

@app.route('/upload', methods=['POST'])
def upload_file():
    if request.method == 'POST':
        cpf = request.form.get('cpf')  # CPF do beneficiário vindo do formulário
        uploaded_file = request.files.get('file')
        
        if not cpf or not uploaded_file:
            return jsonify({'error': 'CPF or file not provided.'}), 400

        allowed_extensions = ['pdf']
        filename = secure_filename(uploaded_file.filename)
        if filename.split('.')[-1].lower() not in allowed_extensions:
            return jsonify({'error': 'Invalid file type. Only PDFs allowed.'}), 400
        
        # Cria uma pasta para o CPF se não existir
        cpf_folder = os.path.join(app.config['UPLOAD_FOLDER'], cpf)
        os.makedirs(cpf_folder, exist_ok=True)
        
        # Salva o arquivo na pasta do CPF
        file_path = os.path.join(cpf_folder, filename)
        uploaded_file.save(file_path)

        return jsonify({'message': 'File uploaded successfully.'}), 201

@app.route('/uploaded-files', methods=['GET'])
def list_uploaded_files():
    files_by_cpf = {}
    try:
        for cpf in os.listdir(app.config['UPLOAD_FOLDER']):
            cpf_folder = os.path.join(app.config['UPLOAD_FOLDER'], cpf)
            if os.path.isdir(cpf_folder):
                files = [{'name': file} for file in os.listdir(cpf_folder) if file.endswith('.pdf')]
                files_by_cpf[cpf] = files
        
        return jsonify({'files_by_cpf': files_by_cpf}), 200
    except OSError as e:
        return jsonify({'error': str(e)}), 500
    
@app.route('/uploaded_files_by_cpf/<cpfRequested>', methods=['GET'])
def list_uploaded_files_by_cpf(cpfRequested):
  files_by_cpf = {}
  try:
    # Get the CPF from the request parameters
    cpf = cpfRequested

    # Iterate over the CPF folders
    for cpf_folder in os.listdir(app.config['UPLOAD_FOLDER']):
      if cpf_folder == cpf:  # Check if the CPF matches
        files = [{'name': file} for file in os.listdir(cpf_folder) if file.endswith('.pdf')]
        files_by_cpf[cpf] = files
        break  # Exit the loop once the matching CPF is found

    return jsonify({'files_by_cpf': files_by_cpf}), 200
  except OSError as e:
    return jsonify({'error': str(e)}), 500

@app.route('/download/<cpf>/<filename>', methods=['GET'])
def download_file(cpf, filename):
    cpf_folder = os.path.join(app.config['UPLOAD_FOLDER'], cpf)
    return send_from_directory(cpf_folder, filename, as_attachment=True)
    
@app.route('/create_atendimento', methods=['POST'])
def create_atendimento():
    data = request.get_json()
    try:
        new_atendimento = Atendimento(
            cpfFunc=data.get('cpfFunc'),
            cpfBen=data.get('cpfBen'),
            assunto=data.get('assunto'),
            data=data.get('data'),
            duracao=data.get('duracao')
        )
        db.session.add(new_atendimento)
        db.session.commit()
        return jsonify({'message': 'Atendimento criado com sucesso'}), 201
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({'error': str(e)}), 400

@app.route('/get_atendimentos', methods=['GET'])
def get_atendimentos():
    try:
        atendimentos = Atendimento.query.all()
        return jsonify([atendimento.to_dictionary() for atendimento in atendimentos]), 200
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({'error': str(e)}), 400

@app.route('/get_atendimento/<int:id>', methods=['GET'])
def get_atendimento(id):    
    atendimento = Atendimento.query.get(id)
    
    if atendimento:
        return jsonify(atendimento.to_dictionary()), 200
    else:
        return jsonify({'error': 'Atendimento não encontrado'}), 404

@app.route('/update_atendimento/<int:id>', methods=['PUT'])
def update_atendimento(id):
    data = request.get_json()
    try:
        atendimento = Atendimento.query.get(id)
        if not atendimento:
            return jsonify({'error': 'Atendimento não encontrado'}), 404

        atendimento.cpfFunc = data.get('cpfFunc', atendimento.cpfFunc)
        atendimento.cpfBen = data.get('cpfBen', atendimento.cpfBen)
        atendimento.assunto = data.get('assunto', atendimento.assunto)
        atendimento.data = data.get('data', atendimento.data)
        atendimento.duracao = data.get('duracao', atendimento.duracao)
        
        db.session.commit()
        return jsonify({'message': 'Atendimento atualizado com sucesso'}), 200
    except Exception as e:
        db.session.rollback()
        print(f"Error: {e}")
        return jsonify({'error': str(e)}), 400

@app.route('/delete_atendimento', methods=['DELETE'])
def delete_atendimento():
    data = request.get_json()
    try:
        atendimento = Atendimento.query.get(data.get('id'))
        if not atendimento:
            return jsonify({'error': 'Atendimento não encontrado'}), 404
        db.session.delete(atendimento)
        db.session.commit()
        return jsonify({'message': 'Atendimento deletado com sucesso'}), 200
    except Exception as e:
        db.session.rollback()
        print(f"Error: {e}")
        return jsonify({'error': str(e)}), 400
    
    
# Configuração do SocketIO
socketio = SocketIO(app, cors_allowed_origins="*")

@socketio.on('connect')
def handle_connect():
    print('Client connected')

@socketio.on('disconnect')
def handle_disconnect():
    print('Client disconnected')

@socketio.on('join')
def handle_join(data):
    room = data['room']
    join_room(room)
    emit('message', {'msg': f'{data["user"]} has joined the room {room}'}, room=room)

@socketio.on('leave')
def handle_leave(data):
    room = data['room']
    leave_room(room)
    emit('message', {'msg': f'{data["user"]} has left the room {room}'}, room=room)

@socketio.on('message')
def handle_message(data):
    room = data['room']
    send({'msg': data['msg'], 'user': data['user']}, room=room)   
    
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(port=5000, debug=True)
    
    