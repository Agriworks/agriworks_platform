from mongoengine import (DynamicDocument, Document, StringField, EmailField, ListField, ValidationError, BooleanField)

class User(DynamicDocument):
    templateName = StringField(max_length=40, required=True)
    author = StringField(max_length=40, required=True)
    headers = ListField(default=[], required=True)