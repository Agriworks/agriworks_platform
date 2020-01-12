from flask import Blueprint, jsonify, send_file, request, make_response
from flask import current_app as app
import app
import json
import math
from bson.objectid import ObjectId
from bson.json_util import dumps
from gridfs import GridFS
from flask_pymongo import PyMongo
from pymongo import MongoClient
#from Controllers.DownloadController import DownloadController
#from Services.AuthenticationService import Authentication
from Models.DataObject import DataObject
from Models.Dataset import Dataset


#Authentication = Authentication()

#MongoDB Configuration
db = app.db.test

#Module that makes it easier to read files from the database using chunks
grid_fs = GridFS(db)

download = Blueprint("DownloadEndpoints",__name__, url_prefix="/download")

@download.route("/", methods=["GET"])
def index():
    #Returns list of datasets
    ret_list = []
    datasetCollection = db.dataset
    for data in datasetCollection.find():
        if data==None:
            return "No datasets found"
        data_name = data["name"]
        data_type = data["type"]
        data_author = data["author"]
        data_id = str(data["_id"])
        datasetObject = {"name":data_name, "type":data_type, "author":data_author, "id":data_id}
        ret_list.append(datasetObject)
        
    return {"datasets": ret_list}

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

@download.route("/<dataset_id>")
def getDataset(dataset_id):
    ret = "{"

    #Get the dataset data
    data = db.dataset.find_one({"_id":ObjectId(dataset_id)})
    if data==None:
        return "Dataset with specified id not found."
    data_name = data["name"]
    data_type = data["type"]
    data_author = data["author"]
    data_id = str(data["_id"])
    json_1 = {"name":data_name, "type":data_type, "author":data_author, "id":data_id}
    json1_str = dumps(json_1)
    ret += json1_str[1:-1]+","

    #Get first data_object to populate the header
    data_object_first = db.data_object.find_one({"dataSetId":ObjectId(dataset_id)})
    first_object = dumps(data_object_first)
    print(first_object)
    headers = []
    for key in data_object_first.keys():
        print (key)
        if key != "_id" and key != "dataSetId":
            headers.append({"text": key, "value": key})
    ret += "\"headers\": "
    ret += dumps(headers) + ","

    #Get all data_objects that belong to dataset
    data_object = db.data_object.find({"dataSetId":ObjectId(dataset_id)})
    data = []

    for row in data_object:
        data_items = {}
        for key in row:
            if key != "_id" and key != "dataSetId":
                if key == "Status":
                    data_items[key] = "HC"
                else:
                    data_items[key] = row[key]
        data.append(data_items)

    ret += "\"data\": "
    ret += dumps(data)

    ret += "}"
    #print(dumps(headers,indent=4))
    #print(dumps(data,indent=4))
    print (ret)
    return ret