
import requests
import sys
import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# ========== Functions ===========

class healthchecker():
    """Monitoring webpages and notify administrator"""
    def __init__(self,  SMTP_HOST, SMTP_PORT, SMTP_USER, SMTP_PASS, MAIL_SENDER, MAIL_RECEIVER, *resources):
        self.emailhost = SMTP_HOST
        self.emailport = SMTP_PORT
        self.emailogin = SMTP_USER
        self.emailpass = SMTP_PASS
        self.emailsender = MAIL_SENDER
        self.emailreceiver = MAIL_RECEIVER
        self.pages = resources

    def fetch_url(self):
        error_pages = []
        for page in resources:
            # print("test " + str(page))
            try:
                response = requests.get(page)
                status_code = response.status_code
                response_time = response.elapsed.total_seconds()
            except Exception:
                error_pages.append(page)
        return error_pages

    def send_report(self, error_pages):
        message = MIMEMultipart("alternative")
        message["Subject"] = "Healtcher report"
        message["From"] = self.emailsender
        message["To"] = self.emailreceiver
        
        text = "Потеряно соединение с следующими узлами:"

        part1 = MIMEText(text + "\n" + str(error_pages), "plain")

        message.attach(part1)

        context = ssl.create_default_context()
        with smtplib.SMTP(self.emailhost, self.emailport) as server:
            server.ehlo()  # Can be omitted
            server.starttls(context=context)
            server.ehlo()  # Can be omitted
            server.login(self.emailogin, self.emailpass)
            server.sendmail(self.emailogin, self.emailreceiver, message.as_string())

# ======== Resources list ========

resources = {
    'http://10.2.1.3:8888',
    'https://example.com',
}

credentials = {
    'SMTP_HOST'    : "mail.example.com",
    'SMTP_PORT'    : "587",
    'SMTP_USER'    : "root@example.com",
    'SMTP_PASS'    : "MySuperPass",
    'MAIL_SENDER'  : "no-reply@example.com",
    'MAIL_RECEIVER': "admin@example.com"
}

# ========== Execute ===========

check = healthchecker(credentials['SMTP_HOST'], credentials['SMTP_PORT'], credentials['SMTP_USER'], credentials['SMTP_PASS'], credentials['MAIL_SENDER'], credentials['MAIL_RECEIVER'], resources)
items = check.fetch_url()
if len(items) > 0:
    check.send_report(items)
else:
    print("All perfect")
