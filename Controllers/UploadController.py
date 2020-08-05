from flask import Blueprint, request
from Response import Response
from Services.UploadService import UploadService
from Services.MailService import MailService 
from Services.AuthenticationService import AuthenticationService
import datetime
from flask_restplus import Api, Resource


upload = Blueprint("UploadController", __name__, url_prefix="/api/upload")
restPlus = Api(upload, doc = "/swagger/")
UploadService = UploadService()
MailService = MailService()
AuthenticationService = AuthenticationService()

@restPlus.route('/') 
class UploadNewFile(Resource):
    @restPlus.doc(
        responses={
            400: "No session detected", 
            400: "Prohibited file type",
            400: "Empty fields detected. Please remove empty values from your dataset and try again." 
        },
        params={
            'SID': {'in': 'cookies', 'required': True},
        }
    )   
    def post(self):
        try:
            uploadRequestDate = str(datetime.datetime.now()).split(".")[0]
            if ("SID" not in request.cookies):
                return Response("No session detected", status=400)
            if ('file' not in request.files):
                return Response("No session detected", status=400)
            if (not UploadService.allowed_file(request.files["file"].filename)):
                return Response("Prohibited file type", status=400) #TODO: Append to response: Dynamically return the types of allowed files
            
            dataset = UploadService.createDataset(request, uploadRequestDate)
            
            return Response(str(dataset.id))
        except ValueError:
            return Response("Empty fields detected. Please remove empty values from your dataset and try again.", status=400) 


@restPlus.route("/getTags/<datasetType>") 
class GetTags(Resource): 
    def get(self, datasetType):
        try:
            return Response(UploadService.getTags(datasetType))
        except:
            return Response("Unable to get tags")
