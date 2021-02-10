from Services.AuthenticationService import AuthenticationService
from flask import current_app
import pandas as pd
AuthenticationService = AuthenticationService()

class DatasetService():
    def __init__(self):
        self.s3 = current_app.awsSession.client('s3')
        return

    """
    @param: dataset document
    @param (optional): Boolean to return object with headers 
    """
    def createDatasetInfoObject(self, dataset, withHeaders=False):
        datasetAuthor = AuthenticationService.getUser(id=dataset.author.id)
        datasetInfoObject = {"name":dataset.name, "legend":dataset.legend, "type":dataset.datasetType, "author": datasetAuthor.getFullname(), "tags": dataset.tags, "id":str(dataset.id), "views": dataset.views}
       
        if (withHeaders):
            headers = []

            #v-table requires headers to be in this format
            #TODO: Update v-table so that we can just pass the headers in as normal without performing any extra work
            
            for header in dataset["keys"]: 
                headerObj = {"text": header, "value": header}
                headers.append(headerObj)
            
            datasetInfoObject["headers"] = headers

        return datasetInfoObject
    
    def buildDatasetObjectsList(self, dataset):
        datasetObjects = []
        for i in range(len(dataset)):
            datasetObjects.append(dict(dataset.iloc[i]))
        return datasetObjects

    def getDataset(self, id):
        rawDataset = self.s3.get_object(Bucket="agriworks-user-datasets", Key=f'{id}.csv')
        return pd.read_csv(rawDataset["Body"], dtype=str).fillna("NO DATA")