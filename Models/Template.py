from mongoengine import (DynamicDocument, Document, StringField, ReferenceField, EmailField, ListField, ValidationError, BooleanField)
from Models.User import User

class Template(DynamicDocument):
    templateName = StringField(max_length=40, required=True)
    author = ReferenceField(User, required=True)
    headers = ListField(default=[], required=True)