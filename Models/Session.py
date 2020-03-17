from mongoengine import Document, StringField, ReferenceField, DateTimeField, UUIDField
from Models.User import User
from datetime import datetime, timedelta


class Session(Document):
    user = ReferenceField(User, required=True)
    sessionId = UUIDField(binary=False, required=True)
    dateCreated = DateTimeField(default=datetime.utcnow) 
    dateExpires = DateTimeField(default=datetime.utcnow() + timedelta(days=30)) #1 month expiration