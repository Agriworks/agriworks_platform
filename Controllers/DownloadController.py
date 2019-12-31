from flask import Blueprint, jsonify, send_file, request, make_response
from flask import current_app as app
import json
from gridfs import GridFS
from flask_pymongo import PyMongo
from pymongo import MongoClient
from Controllers.DownloadController import DownloadController
from Services.AuthenticationService import Authentication


Authentication = Authentication()

#MongoDB Configuration
mongo_client = MongoClient('mongodb://localhost:27017/fileupload')
db = mongo_client['fileupload']

#Module that makes it easier to read files from the database using chunks
grid_fs = GridFS(db)

download = Blueprint("DownloadEndpoints",__name__, url_prefix="/download")

@download.route("/", methods=["GET"])
def index():
    return DownloadController.get()

#Function to get dataset
def getDataset(id) {
    
}

#Displays all of the available files
@download.route("/data", methods=["GET"])
def getAll():
    #set a variable for the database 
    data = mongo.db.fs.files

    #Empty array that collects all of the file information to display
    result = []

    #Loop to gather all of the file information to display 
    for field in data.find():
        result.append({'_id': str(field['_id']), 'filename': field['filename'], 'contentType': field['contentType'], 'md5':field['md5'], 'chunkSize': field['chunkSize'], 'time': field['uploadDate']})
    return jsonify(result)

@download.route('/file/<request>', methods=['GET','POST'])
def file(request):
    #Finds the file in the database from the requested file (comes from the front end)
    grid_fs_file = grid_fs.find_one({'filename': request})
    #Function from flask that makes it easy to create a response to send to the user requesting the download
    response = make_response(grid_fs_file.read())
    response.headers['Content-Type'] = 'application/octet-stream'
    response.headers["Content-Disposition"] = "attachment; filename={}".format(request)
    return response
