from mongoengine import Document, StringField

class Tag(Document):
    name = StringField(required=True)
    datasetType = StringField(required=True)
