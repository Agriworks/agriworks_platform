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
    
    #TODO: Create function to convert all non-compatible data types to compatibles
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
            dataSetTags = request.form.get("tags").split(',')
            dataSetType = request.form.get("type")

            #Remove empty tag
            if (len(dataSetTags) == 1):
                if (dataSetTags[0] == ""):
                    dataSetTags.pop()

            #Read the data in 
            data = pd.read_csv(uploadedFile)
            keys = list(data.columns)
            legend = {} #contains same column values
            nonRepeatedKeys = []

            #Verify that no empty fields exist. 
            if (data.isnull().values.sum() > 0):
                raise ValueError

            #Combine repeated column data into legend
            for i in keys:
                if len(data[i]) <= 1: #if only one row of values, then quit
                    break
                if data[i].nunique() == 1: #if all entries have the same value
                    if str(data[i][0]) != 'nan': #checking to make sure value in not nan
                        legend[i] = data[i][0]
                    if isinstance(data[i][0], numpy.int64):
                        legend[i] = int(data[i][0])
                else:
                    #TODO: Optimize
                    currentNonRepeatedKeyIndex = keys.index(i)
                    nonRepeatedKeys.append(keys[currentNonRepeatedKeyIndex])                    

            #Create dataset object
            dataSet = Dataset(
                name=dataSetName,
                author=dataSetAuthor,
                keys=nonRepeatedKeys,
                legend=legend,
                public=dataSetIsPublic,
                tags=dataSetTags,
                datasetType=dataSetType
            )
            dataSet.save()

            #Populate data into database 
            for i in range(len(data)):
                dataObject = DataObject(dataSetId=dataSet)
                for j in range(len(keys)):
                    currentItem = data.iloc[i][j]
                    if (keys[j] not in legend):                      
                        if (isinstance(currentItem, numpy.int64)):
                            currentItem = int(currentItem) #cast int64 objects to ints 
                        dataObject[keys[j]] = currentItem
                dataObject.save()

            #Go back to the front of the file
            uploadedFile.seek(0)

            #Save to S3
            self.uploadToAWS(dataSet.id, uploadedFile)

            return dataSet #TODO: How do we automatically get a string rep of a mongo object id ?
        
        except ValidationError as e:
            print(e)
            return None

    def uploadToAWS(self, datasetId, file):
        bucketName = "agriworks-user-datasets"
        bucket = s3.Bucket(bucketName)
        filename = str(datasetId) + "." + file.filename.split(".")[1] #filename === datasetId for easy lookups
        bucket.Object(filename).put(Body=file)


    

