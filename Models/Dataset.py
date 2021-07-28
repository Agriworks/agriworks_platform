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

from Models.User import User


class Dataset(DynamicDocument):
    name = StringField(required=True)
    author = ReferenceField(User, required=True)
    keys = ListField(required=True)
    legend = DictField(required=False)
    dateCreated = DateTimeField(default=datetime.now())
    public = BooleanField(required=True)
    tags = ListField()
    datasetType = StringField(required=True)
    columnLabels = ListField(required=True)
    views = IntField(required=True)
    filters = DictField(required=True)

    meta = {
        "indexes": [
            {
                "fields": ["$name", "$keys", "$tags", "$datasetType"],
                "weights": {"title": 5, "keys": 3, "tags": 3, "datasetType": 2},
            }
        ]
    }
