from mongoengine import (Document, StringField, EmailField)

class User(Document):
    firstName = StringField(max_length=20, required=True)
    lastName = StringField(max_length=40, required=True)
    email = EmailField()
    password = StringField() #TODO: convert to encrypted password