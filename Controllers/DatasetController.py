from flask import Blueprint, jsonify, send_file, request, make_response
from Response import Response
from gridfs import GridFS
from flask_pymongo import PyMongo
from pymongo import MongoClient
from Models.DataObject import DataObject
from Models.Dataset import Dataset
from Services.DatasetService import DatasetService
from Models.User import User
from io import StringIO
import boto3
import botocore

DatasetService = DatasetService()

dataset = Blueprint("DatasetEndpoints",__name__, url_prefix="/dataset")

#s3 configuration using boto3
s3 = boto3.client('s3')

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


#TODO: Get any type of file, not just csv. May just need to encode the files without filename. But then need to determine what content_type the file is
@dataset.route('/download/<id>', methods=['GET'])
def file(id):
    try:
        filename = id + ".csv"
        fileFromS3 = s3.get_object(Bucket="agriworks-user-datasets", Key=filename)

        #Body is the content of the file itself
        return Response(fileFromS3["Body"], content_type="text/csv") 

    except botocore.exceptions.ClientError as e:
        if e.response['Error']['Code'] == "404":
            return Response("The object does not exist.")
        else:
            raise