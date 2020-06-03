from flask_mail import Message
from src import mail
from decouple import config


def send_email(recipient,subject,message):
    msg = Message(
        subject = subject,
        recipients = [recipient],
        html = message,
        sender = "mwadimemakokha@gmail.com"
    )
    mail.send(msg)