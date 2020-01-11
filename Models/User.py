from mongoengine import (Document, StringField, EmailField, ValidationError, BooleanField)


class User(Document):
    firstName = StringField(max_length=20, required=True)
    lastName = StringField(max_length=40, required=True)
    email = EmailField()
    admin = BooleanField(default=False)
    password = StringField()  # TODO: convert to encrypted password
