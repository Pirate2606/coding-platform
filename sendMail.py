from flask_mail import Mail, Message
from app import app
from config import SendMail


app.config.from_object(SendMail)
mail = Mail(app)

def send_mail(user_address, message):

    msg = Message('Feedback')
    address = 'RECEIVERS_MAIL'
    msg.recipients.append(str(address))
    msg.body = "ID: " + user_address + "\nMessage : " + message

    mail.send(msg)
