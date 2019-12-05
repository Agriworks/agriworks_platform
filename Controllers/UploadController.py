from flask import Blueprint, flash, request, redirect, jsonify, Response
from flask import current_app as app
from Services.UploadService import UploadService

upload = Blueprint("UploadController", __name__, url_prefix="/upload")
UploadService = UploadService()
    
@upload.route('/', methods=["POST"])
def uploadNewFile():
    if ('file' not in request.files):
        return Response({"Message": "No files were uploaded."}, status=400)

    if (not UploadService.allowed_file(request.files["file"].filename)):
        return Response({"Message": "Prohibited file type."}, status=400) #TODO: Append to response: Dynamically return the types of allowed files

    return UploadService.createDataSetAndDataObjects(request)