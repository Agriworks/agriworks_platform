from mongoengine import DynamicDocument, Document, StringField, ReferenceField, ListField, IntField, DateTimeField, BooleanField, DictField
from datetime import datetime
from Models.User import User
from Models.Dataset import Dataset


class AgriWatchView(DynamicDocument):
    name = StringField(required=True) # by default this should be set to the name of the dataset + the visual type
    author = ReferenceField(User, required=True)
    dateCreated = DateTimeField(default=datetime.now())
    dataset = ReferenceField(Dataset, required=True)
    visualType = StringField(required=True)
    xData = IntField(required=False)
    yData = IntField(required=False)

    meta = {'indexes': [{'fields': ['$name', "$dataset", "$visualType"]}]}
