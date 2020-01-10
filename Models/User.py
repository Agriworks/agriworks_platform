from mongoengine import (Document, StringField, EmailField, ValidationError)


class User(Document):
    firstName = StringField(max_length=20, required=True)
    lastName = StringField(max_length=40, required=True)
    email = EmailField()
    admin = False 
    password = StringField()  # TODO: convert to encrypted password
