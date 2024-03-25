import requests
import sys
import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

file_path = sys.argv[1]
with open(file_path, 'r') as file:
    message_content = file.read()

token = '{{ TELEGRAM_BOT_TOKEN }}'
chat_id = '{{ TELEGRAM_ADMIN_ID }}'
url = f'https://api.telegram.org/bot{token}/sendMessage'

# Отправка сообщения
data = {'chat_id': chat_id, 'text': message_content}
response = requests.post(url, data=data)

# message = MIMEMultipart("alternative")
# message["Subject"] = "Backup status"
# message["From"] = "{{ SERVERNAME }}@{{ SENDEMAIL_DOMAIN }}"
# message["To"] = "{{ SENDEMAIL_RECEIVER }}"

# part1 = MIMEText(message_content, "plain")
# message.attach(part1)

# context = ssl.create_default_context()
# with smtplib.SMTP("{{ SENDEMAIL_HOST }}", "{{ SENDEMAIL_PORT }}") as server:
#     server.ehlo()  # Can be omitted
#     server.starttls(context=context)
#     server.ehlo()  # Can be omitted
#     server.login("{{ SENDEMAIL_LOGIN }}", "{{ SENDEMAIL_PASSWORD }}")
#     server.sendmail("{{ SENDEMAIL_LOGIN }}", "{{ SENDEMAIL_RECEIVER }}", message.as_string())