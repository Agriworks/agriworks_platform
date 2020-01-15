from mongoengine import *
from datetime import datetime
from Models.User import User

class Dataset(Document):
    name = StringField(required=True)
    author = ReferenceField(User, required=True)
    keys = ListField(required=True)
    dateCreated = DateTimeField(default=datetime.now())
    visibility = BooleanField(required=True) #true == public, false == private
    tags = StringField()
    datasetType = StringField(required=True)
        