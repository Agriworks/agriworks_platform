from Services.AuthenticationService import AuthenticationService

AuthenticationService = AuthenticationService()

class DatasetService():
    def __init__(self):
        return

    """
    @param: dataset document
    @param (optional): Boolean to return object with headers 
    """
    def createDatasetInfoObject(self, dataset, withHeaders=False):
        datasetAuthor = AuthenticationService.getUser(id=dataset.author.id)
        datasetInfoObject = {"name":dataset.name, "legend":dataset.legend, "type":dataset.datasetType, "author": datasetAuthor.getFullname(), "tags": dataset.tags, "id":str(dataset.id), "viewCounter": 1}
       
        if (withHeaders):
            headers = []

            #v-table requires headers to be in this format
            #TODO: Update v-table so that we can just pass the headers in as normal without performing any extra work
            
            for header in dataset["keys"]: 
                headerObj = {"text": header, "value": header}
                headers.append(headerObj)
            
            datasetInfoObject["headers"] = headers

        return datasetInfoObject