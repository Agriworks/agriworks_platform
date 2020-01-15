from werkzeug.datastructures import ImmutableMultiDict
from werkzeug.utils import secure_filename
from Models.Dataset import Dataset
from Models.DataObject import DataObject
from Services.AuthenticationService import AuthenticationService
from mongoengine import ValidationError
import pandas as pd
import numpy
import boto3

AuthenticationService = AuthenticationService()

ALLOWED_EXTENSIONS = set(['txt', 'csv'])

s3 = boto3.resource('s3')

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
            dataSetVisibility = True if request.form.get("visibility") == "Public" else False
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
                visibility=dataSetVisibility,
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

            #Go back to the front of the file
            uploadedFile.seek(0)

            #Save to S3
            self.uploadToAWS(dataSet.id, uploadedFile)

            return {"id": str(dataSet.id)} #TODO: How do we automatically get a string rep of a mongo object id ?
        
        except ValidationError as e:
            print(e)
            return None

    def uploadToAWS(self, datasetId, file):
        bucketName = "agriworks-user-datasets"
        bucket = s3.Bucket(bucketName)
        filename = str(datasetId) + "." + file.filename.split(".")[1] #filename === datasetId for easy lookups
        bucket.Object(filename).put(Body=file)


    

