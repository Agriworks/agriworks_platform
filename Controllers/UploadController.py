from flask import Blueprint, flash, request, redirect
from Response import Response
from flask import current_app as app
from Services.UploadService import UploadService
from Services.MailService import MailService 
from Services.AuthenticationService import AuthenticationService
import datetime

upload = Blueprint("UploadController", __name__, url_prefix="/api/upload")
UploadService = UploadService()
MailService = MailService()
AuthenticationService = AuthenticationService()

@upload.route('/', methods=["POST"])
def uploadNewFile():
    try:
        uploadRequestDate = str(datetime.datetime.now()).split(".")[0]
        if ("SID" not in request.cookies):
            return Response("No session detected", status=400)
        if ('file' not in request.files):
            return Response("No files were uploaded", status=400)
        if (not UploadService.allowed_file(request.files["file"].filename)):
            return Response("Prohibited file type", status=400) #TODO: Append to response: Dynamically return the types of allowed files
        
        dataset = UploadService.createDataset(request, uploadRequestDate)
        
        return Response(str(dataset.id))
    except ValueError:
        return Response("Empty fields detected. Please remove empty values from your dataset and try again.", status=400)

@upload.route("/getTags/<datasetType>", methods=["GET"])
def getTags(datasetType):
    try:
        return Response(UploadService.getTags(datasetType))
    except:
        return Response("Unable to get tags")