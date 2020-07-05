from flask import current_app as app
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
mail = SendGridAPIClient(app.config["SENDGRID_KEY"])

class MailService():

    def __init__(self):
        return

    def generateSubject(self, subject):
        return "[Agriworks] " + subject
    
    def generateMessagePrefix(self, user):
        return "<p>Hi " + user.firstName + ", </p>"
    
    def generateMessageBody(self, message):
        return "<p> " + message + "</p>"

    def generateMessageSuffix(self):
        return "<p>Thanks,<br>The Agriworks Team</p>"
    
    def sendMessage(self, user, subject, message):
        messageContent = self.generateMessagePrefix(user) + self.generateMessageBody(message) + self.generateMessageSuffix()
        mail.send(Mail(from_email=app.config["MAIL_USERNAME"], to_emails=user.email, subject=self.generateSubject(subject), html_content=messageContent))

