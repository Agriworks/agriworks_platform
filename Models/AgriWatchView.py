from datetime import datetime

from mongoengine import (
    BooleanField,
    DateTimeField,
    DictField,
    Document,
    DynamicDocument,
    IntField,
    ListField,
    ReferenceField,
    StringField,
)

from Models.Dataset import Dataset
from Models.User import User


class AgriWatchView(DynamicDocument):
    author = ReferenceField(User, required=True)
    dateCreated = DateTimeField(default=datetime.now())
    dataset = ReferenceField(Dataset, required=True)
    visualType = StringField(required=True)
    xData = StringField(required=False)
    yData = StringField(required=False)

    meta = {"indexes": [{"fields": ["$dataset"], "weights": {"dataset": 5}}]}
