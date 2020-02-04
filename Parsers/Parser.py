from Models.Dataset import Dataset
from Models.DataObject import DataObject

class Parser():

    def __init__(self, datasetName, datasetAuthor, datasetPermissions, datasetTags, datasetType, datasetSource):
        self.datasetName = datasetName
        self.datasetAuthor = datasetAuthor
        self.datasetPermissions = True if datasetPermissions == "Public" else False
        self.datasetTags = datasetTags
        self.datasetType = datasetType
        self.datasetSource = datasetSource
        self.datasetId = None
        self.data = None
        self.keys = {}
        self.nonRepeatingKeys = []
        self.legend = {}

    def createDataObjects():
        pass
    
    def parse():
        pass