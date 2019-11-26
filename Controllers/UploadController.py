from flask import Blueprint, flash, request, redirect, jsonify
from flask import current_app as app
from Services.UploadService import UploadService

upload = Blueprint("UploadController", __name__, url_prefix="/upload")
UploadService = UploadService()
    
@upload.route('/', methods=["POST"])
def uploadNewFile():
    if ('file' not in request.files):
        return {"status": "No files were uploaded."}

    if (not UploadService.allowed_file(request.files["file"].filename)):
        return {"status": "Prohibited file type."} #TODO: Append to response: Dynamically return the types of allowed files

    return UploadService.createDataSetAndDataObjects(request)