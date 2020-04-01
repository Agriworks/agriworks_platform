from flask import current_app as app
from flask_mail import Mail, Message
mail = Mail(app)

class MailService():

    def __init__(self):
        return
    
    def generateMessagePrefix(self, user):
        return "<p>Hi " + user.firstName + ", </p>"
    
    def generateMessageBody(self, message):
        return "<p> " + message + "</p>"

    def generateMessageSuffix(self):
        return "<p>Thanks,<br>The Agriworks Team</p>"
    
    def sendMessage(self, user, subject, message):
        messageContent = self.generateMessagePrefix(user) + self.generateMessageBody(message) + self.generateMessageSuffix()
        mail.send(Message(recipients=[user.email], subject=subject, html=messageContent))

