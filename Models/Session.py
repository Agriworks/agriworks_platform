from mongoengine import Document, StringField, ReferenceField, DateTimeField, UUIDField
from uuid import uuid4
from Models.User import User
from datetime import datetime

class Session(Document):
    user = ReferenceField(User, required=True)
    sessionId = UUIDField(binary=False, default=uuid4(), required=True)
    date_created = DateTimeField(default=datetime.utcnow) 
    #TODO: Add expiration date, need to make it expire