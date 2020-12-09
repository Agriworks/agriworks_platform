from mongoengine import DynamicDocument, Document, StringField, ReferenceField, ListField, IntField, DateTimeField, BooleanField, DictField
from datetime import datetime
from Models.User import User
from Models.Dataset import Dataset


class AgriWatchView(DynamicDocument):
    author = ReferenceField(User, required=True)
    dateCreated = DateTimeField(default=datetime.now())
    dataset = ReferenceField(Dataset, required=True)
    visualType = StringField(required=True)
    xData = StringField(required=False)
    yData = StringField(required=False)

    meta = {'indexes': [{'fields': ["$dataset"], 'weights': {'dataset': 5}}]}
