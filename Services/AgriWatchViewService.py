from Models.AgriWatchView import AgriWatchView
from Models.Dataset import Dataset
from Services.AuthenticationService import AuthenticationService
from Services.DatasetService import DatasetService
from mongoengine import ValidationError

AuthenticationService = AuthenticationService()

class AgriWatchViewService():
    def __init__(self):
        return

    def createView(self, request):
        print("Creating view")
        try:
            # Get the user to establish view ownership
            user = AuthenticationService.verifySessionAndReturnUser(request.cookies["SID"])
            if (not user):
                return {"message": "Invalid session", "status": 400}

            # Get the dataset to link view to dataset
            #problem if the dataset name is not unique
            datasetId = request.form.get("dataset")
            dataset = Dataset.objects.get(id=datasetId)
            if (not dataset):
                return {"message": "Invalid dataset ID", "status": 400}

            viewAuthor = user
            viewDataset = dataset
            viewVisualtype = request.form.get("visualType")
            viewXData = request.form.get("xData")
            viewYData = request.form.get("yData")

            # Create and save view object
            view = AgriWatchView(
                author = viewAuthor,
                dataset = viewDataset,
                visualType = viewVisualtype,
                xData = viewXData,
                yData = viewYData
            )
            view.save()

            return view

        except ValidationError as e:
            print(e)
            return None

    # create object with all view info
    def makeViewObject(self, view):
        viewDataset = Dataset.objects.get(id=view.dataset.id)
        viewObject = {
            "dataset": viewDataset.name,
            "visualType": view.visualType,
            "xData": view.xData,
            "yData": view.yData 
        }
        return viewObject