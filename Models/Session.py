from datetime import datetime, timedelta

from mongoengine import DateTimeField, Document, ReferenceField, StringField, UUIDField

from Models.User import User


class Session(Document):
    user = ReferenceField(User, required=True)
    sessionId = UUIDField(binary=False, required=True)
    dateCreated = DateTimeField(default=datetime.utcnow)
    dateExpires = DateTimeField(
        default=datetime.utcnow() + timedelta(days=30)
    )  # 1 month expiration
