from Services.AuthenticationService import AuthenticationService

AuthenticationService = AuthenticationService()

class DatasetService():
    def __init__(self):
        return

    """
    @param: dataset document
    """
    def createDatasetInfoObject(self, dataset):
        datasetAuthor = AuthenticationService.getUser(id=dataset.author.id)
        return {"name":dataset.name, "type":dataset.datasetType, "author": datasetAuthor.getFullname(), "id":str(dataset.id)}