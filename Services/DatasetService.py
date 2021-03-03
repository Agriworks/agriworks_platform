from Services.AuthenticationService import AuthenticationService
from Models.Dataset import Dataset
from Models.User import User
import json

AuthenticationService = AuthenticationService()

class DatasetService():
    def __init__(self):
        return

    """
    @param: dataset document
    @param (optional): Boolean to return object with headers 
    """
    def createDatasetInfoObject(self, dataset, withHeaders=False, userEmail=""):
        datasetAuthor = AuthenticationService.getUser(id=dataset.author.id)
        allowToEdit = False
        if userEmail == datasetAuthor.email:
            allowToEdit = True
        datasetInfoObject = {"name":dataset.name, 
                             "legend":dataset.legend, 
                             "type":dataset.datasetType, 
                             "author": datasetAuthor.getFullname(), 
                             "tags": dataset.tags, "id":str(dataset.id), 
                             "views": dataset.views, 
                             "columnLabels": dataset.columnLabels, 
                             "allowToEdit": allowToEdit}
       
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

    def changeLabel(self, request):
        datasetID = request.form.get("datasetID")
        user = request.form.get("user")
        columnLabels = json.loads(request.form.get("labels"))
        try:
            dataset = Dataset.objects.get(id=datasetID)
            author = User.objects.get(id=dataset.author.id)
            if author.email != user:
                return False
            dataset.columnLabels = columnLabels
            dataset.save()
            return True
        except:
            return False

