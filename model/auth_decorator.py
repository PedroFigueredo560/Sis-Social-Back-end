from functools import wraps
from flask import request, jsonify
import jwt
from database import app  # Certifique-se de que 'app' está sendo importado corretamente

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization')
        if not token:
            return jsonify({'message': 'Token is missing!'}), 403

        try:
            if 'Bearer ' in token:
                token = token.split('Bearer ')[1]  # Remove o prefixo 'Bearer'
            data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
            request.user = data  # Guarda as informações do usuário no contexto da requisição
        except jwt.ExpiredSignatureError:
            return jsonify({'message': 'Token has expired!'}), 403
        except jwt.InvalidTokenError:
            return jsonify({'message': 'Token is invalid!'}), 403

        return f(*args, **kwargs)
    return decorated
