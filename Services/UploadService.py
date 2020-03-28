from werkzeug.datastructures import ImmutableMultiDict
from werkzeug.utils import secure_filename
from Models.Dataset import Dataset
from Models.DataObject import DataObject
from Models.Tag import Tag
from Services.AuthenticationService import AuthenticationService
from Services.MailService import MailService
from mongoengine import ValidationError
from flask import current_app
import pandas as pd
import numpy
import datetime


AuthenticationService = AuthenticationService()
MailService = MailService()

ALLOWED_EXTENSIONS = set(['txt', 'csv'])

s3 = current_app.awsSession.resource('s3')

class UploadService():

    def __init__(self):
        self.largeFileThreshold = 1500
        return
    
    #Function that checks the file type 
    def allowed_file(self, filename):
        return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

    #TODO: Verify that the user that is uploading this dataset is logged in. 
    def createDataset(self, request, uploadTime):
        try:
            #keep track of when request was made 
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

            keys = list(pd.read_csv(uploadedFile).columns)

            #Create and save dataset object
            dataset = Dataset(
                name=dataSetName,
                author=dataSetAuthor,
                keys=keys,
                public=dataSetIsPublic,
                tags=dataSetTags,
                datasetType=dataSetType, 
                views=1
            )
            dataset.save()

            #Go back to the front of the file
            uploadedFile.seek(0)

            #Save to S3
            self.uploadToAWS(dataset.id, uploadedFile)
            
            uploadCompletedDate = str(datetime.datetime.now()).split(".")[0]
            
            MailService.sendMessage(user, "Dataset successfully uploaded", "Your <b>{}</b> dataset has finished processing. <br> <br> <b>Upload Submitted</b>: {} <br> <br> <b>Upload Completed</b>: {}<br> <br> <b> Link below to view your dataset: </b> <br> <a href ='agri-works.org/dataset/{}'>agri-works.org/dataset/{}</a>.".format(dataset.name, uploadTime, uploadCompletedDate, dataset.id, dataset.id))
            return dataset
            
        except ValidationError as e:
            print(e)
            return None
    
    def tagExist(self, tag):
        try:        
            tag = Tag.objects.get(name=tag.name, datasetType=tag.datasetType)
            tag.noOfEntries += 1
            tag.save()
            return True
        except:
            return False
    
    def getTags(self, datasetType):
        tags = []  

        # get first 10 most used tags for the datasetType
        for tag in Tag.objects(datasetType=datasetType).order_by('noOfEntries')[:10]:
            tags.append(tag.name)
        return tags
    
    def uploadToAWS(self, datasetId, file):
        bucketName = "agriworks-user-datasets"
        bucket = s3.Bucket(bucketName)
        filename = str(datasetId) + "." + file.filename.split(".")[1] #filename === datasetId for easy lookups
        bucket.Object(filename).put(Body=file)


    

