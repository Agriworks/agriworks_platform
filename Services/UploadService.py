from werkzeug.datastructures import ImmutableMultiDict
from werkzeug.utils import secure_filename
from Models.Dataset import Dataset
from Models.DataObject import DataObject
import pandas as pd
import numpy
from mongoengine import ValidationError
from Services.AuthenticationService import AuthenticationService

AuthenticationService = AuthenticationService()

ALLOWED_EXTENSIONS = set(['txt', 'csv'])

class UploadService():

    def __init__(self):
        return
    
    #Function that checks the file type 
    def allowed_file(self, filename):
        return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
    
    #TODO: Catch errors (ex. Catching a mongovalidation error. We don't want to present the client with the raw error but instead we
    #want to process the error and return the appropriate error message.
    #TODO: Verify that the user that is uploading this dataset is logged in. 
    def createDataSetAndDataObjects(self, request):
        try:
            user = AuthenticationService.verifySessionAndReturnUser(request.cookies["SID"])

            if (not user):
                return {"message": "Invalid session", "status": 400}

            #TODO: verify that these parameters exist
            uploadedFile = request.files['file']
            dataSetName = request.form.get("name")
            dataSetAuthor = user
            dataSetIsPublic = True if request.form.get("permissions") == "Public" else False
            dataSetTags = request.form.get("tags")
            dataSetType = request.form.get("type")

            #Read the data in 
            data = pd.read_csv(uploadedFile)
            keys = list(data.columns)

            #Create dataset object
            dataSet = Dataset(
                name=dataSetName,
                author=dataSetAuthor,
                keys=keys,
                public=dataSetIsPublic,
                tags=dataSetTags,
                datasetType=dataSetType
            )
            dataSet.save()
            
            #Populate data into database #TODO: How do we read data in without having to convert to mongodb acceptable types ? 
            for i in range(len(data)):
                dataObject = DataObject(dataSetId=dataSet)
                for j in range(len(keys)):
                    currentItem = data.iloc[i][j]
                    if (isinstance(currentItem, numpy.int64)):
                        currentItem = int(currentItem) #cast int64 objects to ints 
                    dataObject[keys[j]] = currentItem
                dataObject.save()

            return {"id": str(dataSet.id)} #TODO: How do we automatically get a string rep of a mongo object id ?

        except ValidationError as e:
            print(e)
            return None