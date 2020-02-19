from flask import Blueprint, flash, request, redirect
from Response import Response
from flask import current_app as app
from Services.UploadService import UploadService

upload = Blueprint("UploadController", __name__, url_prefix="/upload")
UploadService = UploadService()
    
@upload.route('/', methods=["POST"])
def uploadNewFile():
    
    if ("SID" not in request.cookies):
        return Response("No session detected", status=400)
    if ('file' not in request.files):
        return Response("No files were uploaded", status=400)
    if (not UploadService.allowed_file(request.files["file"].filename)):
        return Response("Prohibited file type", status=400) #TODO: Append to response: Dynamically return the types of allowed files
    
    return Response(UploadService.createDataSetAndDataObjects(request))

