from mongoengine import Document, StringField, IntField

class Tag(Document):
    name = StringField(required=True)
    datasetType = StringField(required=True)
    noOfEntries = IntField(required=True, default=1)
