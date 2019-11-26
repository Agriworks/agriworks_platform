from mongoengine import *
from datetime import datetime

class Dataset(Document):
    Name = StringField(required=True)
    DateCreated = DateTimeField(default=datetime.now())
    Description = StringField()
    Keys = ListField(required=True)