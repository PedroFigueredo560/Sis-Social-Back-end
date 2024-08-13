from flask import Flask
from flask_mail import Mail, Message

app = Flask(__name__)
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USERNAME'] = 'email'
app.config['MAIL_PASSWORD'] = 'senha'
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False

mail = Mail(app)

@app.route('/send_email')
def send_email():
    try:
        msg = Message("Teste de E-mail", sender="email", recipients=["recipient@example.com"])
        msg.body = "Texto com acentuação: áéíóú"
        mail.send(msg)
        return "E-mail enviado com sucesso!"
    except Exception as e:
        return f"Erro ao enviar e-mail: {e}"

if __name__ == '__main__':
    app.run(port=5001, debug=True)
