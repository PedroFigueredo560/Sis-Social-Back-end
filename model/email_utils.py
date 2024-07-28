# import smtplib
# from email.mime.text import MIMEText
# from email.mime.multipart import MIMEMultipart

# def send_email(to_email, subject, body):
#     smtp_server = 'smtp.your-email-provider.com'
#     smtp_port = 587
#     smtp_username = 'your-email@example.com'
#     smtp_password = 'your-email-password'

#     msg = MIMEMultipart()
#     msg['From'] = smtp_username
#     msg['To'] = to_email
#     msg['Subject'] = subject

#     msg.attach(MIMEText(body, 'plain'))

#     try:
#         with smtplib.SMTP(smtp_server, smtp_port) as server:
#             server.starttls()
#             server.login(smtp_username, smtp_password)
#             server.sendmail(msg['From'], msg['To'], msg.as_string())
#     except Exception as e:
#         print(f"Error sending email: {e}")
