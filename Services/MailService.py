from flask_mail import Mail, Message
mail = Mail(app)

class MailService():

    def generateMessagePrefix(user):
        return "<p>Hi there, " + user.firstName " </p>"
    
    def generateMessageBody(message):
        return "<p> " + message + "</p>"

    def generateMessageSuffix():
        return "<p>Thanks,<br>The Agriworks Team</p>"
    
    def sendMessage(user, subject, message):
        messageContent = generateMessagePrefix(user) + generateMessageBody(message) + generateMessageSuffix
        mail.send(Message(recipients=[user.email], subject=subject, html=messageContent))
