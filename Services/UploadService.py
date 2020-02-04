from Services.AuthenticationService import AuthenticationService
from Parsers.csv import CSVParser
from mongoengine import ValidationError

import boto3

AuthenticationService = AuthenticationService()
CSVParser = CSVParser()

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
        
            # Init parser
            # Get appropriate parser here
            parser = CSVParser()
            parser.parse()

            #Save to S3
            self.uploadToAWS(parser.datasetId, request.files["file"])
            
            return {"id": str(datasetObject.id)} #TODO: How do we automatically get a string rep of a mongo object id ?
        
        except ValidationError as e:
            print(e)
            return None

    def uploadToAWS(self, datasetId, file):
        bucketName = "agriworks-user-datasets"
        bucket = s3.Bucket(bucketName)
        filename = str(datasetId) + "." + file.filename.split(".")[1] #filename === datasetId for easy lookups
        bucket.Object(filename).put(Body=file)


    

