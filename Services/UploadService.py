from werkzeug.datastructures import ImmutableMultiDict
from werkzeug.utils import secure_filename
from Models.Dataset import Dataset
from Models.DataObject import DataObject
import pandas as pd
import numpy
from mongoengine import ValidationError

ALLOWED_EXTENSIONS = set(['txt', 'csv'])

class UploadService():

    def __init__(self):
        return
    
    #Function that checks the file type 
    def allowed_file(self, filename):
        return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
    
    #TODO: Catch errors (ex. Catching a mongovalidation error. We don't want to present the client with the raw error but instead we
    #want to process the error and return the appropriate error message.
    #TODO: Attach dataset to user. Verify that the user that is uploading this dataset is logged in. 
    #TODO: Add private/public field to Dataset object 
    def createDataSetAndDataObjects(self, request):
        try:
            #Get parameters
            uploadedFile = request.files['file']
            dataSetName = request.form.get("name")
            dataSetDescription = request.form.get("description")
            
            #Read the data in 
            data = pd.read_csv(uploadedFile)
            keys = list(data.columns)

            #Create dataset object
            dataSet = Dataset(Name=dataSetName,Description=dataSetDescription,Keys=keys)
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
            
            return {"status": (dataSetName + " was successfully uploaded")}

        except ValidationError:
            return {"status": "Mongoengine validation error" }