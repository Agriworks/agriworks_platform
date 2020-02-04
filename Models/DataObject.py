from mongoengine import LazyReferenceField, DynamicDocument
from Models.Dataset import Dataset

# One data object === one row of data


class DataObject(DynamicDocument):
    dataSetId = LazyReferenceField(Dataset)
    # Dynamically set keys and values
