from mongoengine import *
from Models.Dataset import Dataset

class DataObject(DynamicDocument):
    dataSetId = LazyReferenceField(Dataset)
    #Dynamically set keys and values