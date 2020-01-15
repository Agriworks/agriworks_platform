from mongoengine import (Document, StringField, EmailField, ValidationError, BooleanField)

class User(Document):
    firstName = StringField(max_length=40, required=True)
    lastName = StringField(max_length=40, required=True)
    email = EmailField(required=True)
    isAdmin = BooleanField(default=False)
    password = StringField(required=True)  # TODO: convert to binary field
