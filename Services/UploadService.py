from Models.Dataset import Dataset
from Models.Tag import Tag
from Services.AuthenticationService import AuthenticationService
from Services.MailService import MailService
from mongoengine import ValidationError
from flask import current_app as app
import pandas as pd
import datetime
import json

AuthenticationService = AuthenticationService()
MailService = MailService()

ALLOWED_EXTENSIONS = set(['txt', 'csv'])

s3 = app.awsSession.resource('s3')

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
            dataSetIsPublic = True if request.form.get(
                "permissions") == "Public" else False
            dataSetTags = request.form.get("tags").split(',')
            dataSetType = request.form.get("type")
            dataSetColumnData = json.loads(request.form.get("columnData"))
            dataSetTimeGranularity = request.form.get("timeGranularity")
            dataSetLocationGranularity = request.form.get("locationGranularity")

            if (len(dataSetTags) == 1):
                if (dataSetTags[0] == ""):
                    dataSetTags.pop()

            data = pd.read_csv(uploadedFile)
            keys = list(data.columns)

            if (data.isnull().values.sum() > 0 ):
                raise ValueError
        
            #Add new tags to collection
            for tag in dataSetTags:
                newTag = Tag(
                    name=tag,
                    datasetType=dataSetType
                )
                newTag.validate()
                if not self.tagExist(newTag):
                    newTag.save()

            #Create and save dataset object
            dataset = Dataset(
                name=dataSetName,
                author=dataSetAuthor,
                keys=keys,
                public=dataSetIsPublic,
                tags=dataSetTags,
                datasetType=dataSetType,
                columnData=dataSetColumnData,
                timeGranularity=dataSetTimeGranularity,
                locationGranularity=dataSetLocationGranularity,
                views=1
            )
            dataset.save()

            #Go back to the front of the file
            uploadedFile.seek(0)

            #Save to S3
            self.uploadToAWS(dataset.id, uploadedFile)
            
            uploadCompletedDate = str(datetime.datetime.now()).split(".")[0]

            headline = f"Your <b>{dataset.name}</b> dataset has finished processing. <br> <br> "
            uploadString = f"<b>Upload Received</b>: {uploadTime} <br> <br> <b>Upload Completed</b>: {uploadCompletedDate}<br> <br>"
            datasetLink = f"<b> Link below to view your dataset: </b> <br> <a href ='{app.rootUrl}/dataset/{dataset.id}'>{app.rootUrl}/dataset/{dataset.id}</a>."
            formattedMessage = headline + uploadString + datasetLink
            MailService.sendMessage(user, "Dataset successfully uploaded", formattedMessage)
            
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
        # filename === datasetId for easy lookups
        filename = str(datasetId) + "." + file.filename.split(".")[1]
        bucket.Object(filename).put(Body=file)