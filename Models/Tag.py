from mongoengine import Document, IntField, StringField


class Tag(Document):
    name = StringField(required=True)
    datasetType = StringField(required=True)
    noOfEntries = IntField(required=True, default=1)
