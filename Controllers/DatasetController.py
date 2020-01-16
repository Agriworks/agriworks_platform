from flask import Blueprint, jsonify, send_file, request, make_response
from Response import Response
from gridfs import GridFS
from flask_pymongo import PyMongo
from pymongo import MongoClient
from Models.DataObject import DataObject
from Models.Dataset import Dataset
from Services.DatasetService import DatasetService
from Models.User import User

DatasetService = DatasetService()

dataset = Blueprint("DatasetEndpoints",__name__, url_prefix="/dataset")

#TODO: return only public datasets and datasets which the user owns
@dataset.route("/", methods=["GET"])
def get():
    #Returns list of datasets 
    ret_list = []
    datasets = Dataset.objects
    for dataset in datasets:
        if dataset == None:
            return Response("No datasets found", status=400)

        ret_list.append(DatasetService.createDatasetInfoObject(dataset))

    return jsonify(ret_list)


#TODO: ensure that only authorized users can access a dataset
@dataset.route("/<dataset_id>")
def getDataset(dataset_id):

    dataset = Dataset.objects.get(id=dataset_id)
    
    if dataset==None:
        return Response("Dataset with specified id not found.", status=400)

    datasetObj = DatasetService.createDatasetInfoObject(dataset, withHeaders=True)

    #Get all data_objects that belong to dataset
    data_objects = DataObject.objects(dataSetId=dataset_id)
    data = []

    for row in data_objects:
        data_items = {}
        for key in row:
            if key != "id" and key != "dataSetId":
                if key == "Status":
                    data_items[key] = "HC"
                else:
                    data_items[key] = row[key]
        data.append(data_items)

    datasetObj["data"] = data
    return jsonify(datasetObj)

#TODO: only return public datasets and the datasets that belong to the user
@dataset.route("/search/<searchQuery>", methods=['GET'])
def search(searchQuery):
    datasets = []
    try:
        if searchQuery == "" or searchQuery == " ":
            raise
        else:
            matchedAuthors = User.objects.search_text(searchQuery)
            for user in matchedAuthors:
                try:
                    correspondingDataset = Dataset.objects.get(author=user.id)
                    datasets.append(DatasetService.createDatasetInfoObject(correspondingDataset))
                except:
                    pass

            matchedDatasets = Dataset.objects.search_text(searchQuery).order_by('$text_score')
            for dataset in matchedDatasets:
                datasets.append(DatasetService.createDatasetInfoObject(dataset))

            return jsonify(datasets)
    except:
        return Response("No matching datasets found for query")

#--------------------------------------------------------------------
# TODO: This needs to be modified to query S3, not gridfs in mongodb

#MongoDB Configuration
#db = app.db.test

#Module that makes it easier to read files from the database using chunks
#grid_fs = GridFS(db)

#Displays all of the available files
@dataset.route("/data", methods=["GET"])
def getAll():
    #set a variable for the database 
    data = mongo.db.fs.files

    #Empty array that collects all of the file information to display
    result = []

    #Loop to gather all of the file information to display 
    for field in data.find():
        result.append({'_id': str(field['_id']), 'filename': field['filename'], 'contentType': field['contentType'], 'md5':field['md5'], 'chunkSize': field['chunkSize'], 'time': field['uploadDate']})
    return jsonify(result)

@dataset.route('/file/<request>', methods=['GET','POST'])
def file(request):
    #Finds the file in the database from the requested file (comes from the front end)
    grid_fs_file = grid_fs.find_one({'filename': request})
    #Function from flask that makes it easy to create a response to send to the user requesting the download
    response = make_response(grid_fs_file.read())
    response.headers['Content-Type'] = 'application/octet-stream'
    response.headers["Content-Disposition"] = "attachment; filename={}".format(request)
    return response


