import smtplib
from email.mime.text import MIMEText

def send_test_email(to_email):
    from_email = "jainer469@gmail.com"
    subject = "Teste de Envio de E-mail"
    body = "Este é um teste para verificar se o e-mail está sendo enviado corretamente."
    
    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = from_email
    msg['To'] = to_email

    try:
        with smtplib.SMTP('smtp.dominio.com', 587) as server:
            server.starttls()
            server.login('jainer469@gmail.com', 'sua_senha')
            server.send_message(msg)
            print(f"E-mail de teste enviado para {to_email}")
    except Exception as e:
        print(f"Erro ao enviar e-mail: {e}")

# Teste o envio
send_test_email('jainer469@gmail.com')
