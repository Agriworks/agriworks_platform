from mongoengine import Document, StringField, ReferenceField, DateField
from uuid import uuid4
from Models.User import User

class Session(Document):
    sessionId = StringField(str(uuid4()))
    user = ReferenceField(User)
    #TODO: Add expiration date