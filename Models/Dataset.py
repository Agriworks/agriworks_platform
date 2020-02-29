from mongoengine import Document, StringField, ReferenceField, ListField, DateTimeField, BooleanField, DictField, IntField
from datetime import datetime
from Models.User import User


class Dataset(Document):
    name = StringField(required=True)
    author = ReferenceField(User, required=True)
    keys = ListField(required=True)
    legend = DictField(required=False)
    dateCreated = DateTimeField(default=datetime.now())
    public = BooleanField(required=True)
    tags = ListField()
    datasetType = StringField(required=True)
    viewCounter = IntField(required = True)

    meta = {'indexes': [{'fields': ['$name', "$keys", "$tags", "$datasetType"], 'weights': {
        'title': 5, 'keys': 3, 'tags': 3, 'datasetType': 2}}]}
