from mongoengine import *
from datetime import datetime
from Models.User import User

class Dataset(Document):
    name = StringField(required=True)
    author = ReferenceField(User, required=True)
    keys = ListField(required=True)
    legend = DictField(required=True)
    dateCreated = DateTimeField(default=datetime.now())
    public = BooleanField(required=True)
    tags = StringField()
    datasetType = StringField(required=True)
    
    meta = {'indexes': [{'fields': ['$name', "$keys", "$tags", "$datasetType"],'weights': {'title': 5, 'keys':3, 'tags': 3, 'datasetType': 2 }}]}