from flask import Blueprint, flash, request, redirect, jsonify
from threading import Thread
from Response import Response
from flask import current_app as app
from Services.UploadService import UploadService

upload = Blueprint("UploadController", __name__, url_prefix="/upload")
UploadService = UploadService()
    
@upload.route('/', methods=["POST"])
def uploadNewFile():
    try:
        if ("SID" not in request.cookies):
            return Response("No session detected", status=400)
        if ('file' not in request.files):
            return Response("No files were uploaded", status=400)
        if (not UploadService.allowed_file(request.files["file"].filename)):
            return Response("Prohibited file type", status=400) #TODO: Append to response: Dynamically return the types of allowed files
        
        #check file size
        if len(request.files['file'].read()) > 1:#0 * 1024 * 1024: # if larger than 10MB
            dataset = UploadService.threadCreateDataSetAndDataObjects(request)
            return jsonify({'started': True})

        dataset = UploadService.createDataSetAndDataObjects(request)
        
        return Response(str(dataset.id))
    except ValueError:
        return Response("Empty fields detected. Please remove empty values from your dataset and try again.", status=400)