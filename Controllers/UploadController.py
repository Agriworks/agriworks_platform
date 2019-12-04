from flask import Blueprint, flash, request, redirect, jsonify, abort
from flask import current_app as app
from Services.UploadService import UploadService

upload = Blueprint("UploadController", __name__, url_prefix="/upload")
UploadService = UploadService()
    
@upload.route('/', methods=["POST"])
def uploadNewFile():
    if ('file' not in request.files):
        abort(400, {"Message": "No files were uploaded."})
        return {"status": "No files were uploaded."} #Not sure if this return is still needed

    if (not UploadService.allowed_file(request.files["file"].filename)):
        abort(400, {"Message": "Prohibited file type."})
        return {"status": "Prohibited file type."} #TODO: Append to response: Dynamically return the types of allowed files

    return UploadService.createDataSetAndDataObjects(request)