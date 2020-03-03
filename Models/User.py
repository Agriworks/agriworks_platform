from mongoengine import (Document, StringField, EmailField, ValidationError, BooleanField, ListField)

class User(Document):
    firstName = StringField(max_length=40, required=True)
    lastName = StringField(max_length=40, required=True)
    email = EmailField(required=True)
    isAdmin = BooleanField(default=False)
    password = StringField(required=True)
    recentDatasets = ListField(default=[])

    def getFullname(self):
        return self.firstName + " " + self.lastName
    
    meta = {'indexes': [{'fields': ['$firstName', "$lastName"]}]}

