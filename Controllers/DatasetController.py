from flask import Blueprint, jsonify, send_file, request, make_response, current_app, json
from Response import Response
from gridfs import GridFS
from flask_pymongo import PyMongo
from pymongo import MongoClient
from Models.DataObject import DataObject
from Models.Dataset import Dataset
from Services.DatasetService import DatasetService
from Services.AuthenticationService import AuthenticationService
from Models.User import User
from io import StringIO
import boto3
import botocore
import time
import pandas as pd
from uuid import uuid4

DatasetService = DatasetService()
AuthenticationService = AuthenticationService()

dataset = Blueprint("DatasetEndpoints", __name__, url_prefix="/api/dataset")

s3 = current_app.awsSession.client('s3')

DatasetCache = {}

# TODO: return only public datasets and datasets which the user owns
@dataset.route("/list/<pageNumber>", methods=["GET"])
def get(pageNumber):
    ret_list = []
    datasets = []

    if pageNumber == "all":
        datasets = Dataset.objects
    elif pageNumber == "0":
        datasets = Dataset.objects[:16]
    else:
        datasetIndex = 16 + 12 * (int(pageNumber) - 1)
        datasets = Dataset.objects[datasetIndex: datasetIndex + 12]

    if len(datasets) == 0:
        return Response("No datasets matching the query were found", status=400)

    for dataset in datasets:
        ret_list.append(DatasetService.createDatasetInfoObject(dataset))

    return Response(ret_list)

# returns the users datasets
@dataset.route("/user/", methods=["GET"])
def getUsersDataset():
    ret_list = []
    user = AuthenticationService.verifySessionAndReturnUser(
        request.cookies["SID"])
    datasets = Dataset.objects.filter(author=user)
    for dataset in datasets:
        if dataset == None:
            return Response("No datasets found", status=400)
        ret_list.append(DatasetService.createDatasetInfoObject(dataset))
    return jsonify(ret_list)

# TODO: ensure that only authorized users can access a dataset
@dataset.route("/metadata/<dataset_id>", methods=["GET"])
def getDataset(dataset_id):
    dataset = Dataset.objects.get(id=dataset_id)

    if dataset == None:
        return Response("Unable to retrieve dataset information. Please try again later.", status=400)

    Dataset.objects(id=dataset_id).update_one(inc__views=1)
    AuthenticationService.updateRecentDatasets(request.cookies["SID"],dataset_id)
    return Response(DatasetService.createDatasetInfoObject(dataset, withHeaders=True))

# Delete a specific dataset
@dataset.route("/<dataset_id>", methods=["DELETE"])
def deleteDataset(dataset_id):
    dataset = Dataset.objects.get(id=dataset_id)

    if dataset == None:
        return Response("Dataset does not exist.", status=400)

    try: 
        s3.delete_object(Bucket="agriworks-user-datasets", Key=dataset_id + ".csv")
        dataset.delete()
        return Response("Succesfully deleted dataset.", status=200)
    except:
        return Response("Could not delete dataset.", status=500)

# TODO: only return public datasets and the datasets that belong to the user
@dataset.route("/search/<searchQuery>", methods=['GET'])
def search(searchQuery):
    datasets = []
    browseURL = "browse"
    manageURL = "manage"
    referrerURL = request.headers["referer"].split('/')[-1]

    matchedDatasets = []
    typeUser = None

    try:
        if searchQuery == "" or searchQuery == " ":
            raise
        else:
            #Perform search only on user datasets
            if referrerURL == manageURL:
                user = AuthenticationService.verifySessionAndReturnUser(
                    request.cookies["SID"])
                userDatasets = Dataset.objects.filter(author=user)
                matchedDatasets = userDatasets.search_text(
                    searchQuery).order_by('$text_score')
                typeUser = True
            #Perform search on all datasets
            elif referrerURL == browseURL:
                matchedDatasets = Dataset.objects.search_text(
                    searchQuery).order_by('$text_score')
                typeUser = False
            else:
                # invalid referrer url
                return Response("Error processing request. Please try again later.", status=400)

        for dataset in matchedDatasets:
            datasets.append(DatasetService.createDatasetInfoObject(dataset))

        if typeUser:
            return Response({"datasets": datasets, "type": "user"})
        return Response({"datasets": datasets, "type": "all"})

    except:
        return Response("Unable to retrieve datasets with the given search parameter.", status=400)


# TODO: Get any type of file, not just csv. May just need to encode the files without filename. But then need to determine what content_type the file is
@dataset.route('/download/<id>', methods=['GET'])
def file(id):
    try:
        filename = id + ".csv"
        fileFromS3 = s3.get_object(
            Bucket="agriworks-user-datasets", Key=filename)

        # Body is the content of the file itself
        return Response(fileFromS3["Body"], content_type="text/csv")

    except botocore.exceptions.ClientError as e:
        if e.response['Error']['Code'] == "404":
            return Response("The object does not exist.")
        else:
            raise


# return the most popular datasets
@dataset.route("/popular", methods=["GET"])
def popular(): 
    try: 
        ret_list = []
        # sorts the datasets by ascending order
        datasets = Dataset.objects.order_by("-views")[:5]
        for dataset in datasets:
            if dataset == None:
                return Response("No datasets found", status=400)
            ret_list.append(DatasetService.createDatasetInfoObject(dataset))
        return Response(ret_list)
    except:
        return Response("Couldn't retrieve popular datasets", status=400)


# return the users most recent datasets 
@dataset.route("/recent", methods=["GET"])
def recent(): 
    try: 
        ret_list = []
        # use cookies to retrieve user
        user = AuthenticationService.verifySessionAndReturnUser(
            request.cookies["SID"])
        recentDatasetIds = user.recentDatasets[:5]
        # retrieve the actual datasets from these ids
        for datasetId in recentDatasetIds:
            try:
                ret_list.append(DatasetService.createDatasetInfoObject(
                    Dataset.objects.get(id=datasetId)))
            except:
                continue
        return Response(ret_list)

    except Exception as e:
        return Response("Couldn't retrieve recent datasets", status=400)

# returns the newest datasets created by the user 
@dataset.route("/new", methods=["GET"])
def new(): 
    try: 
        ret_list = []
        user = AuthenticationService.verifySessionAndReturnUser(
            request.cookies["SID"])
        # get users datasets by date created and sort by descending order
        newDatasets = Dataset.objects(author=user).order_by("-dateCreated")[:5]
        for dataset in newDatasets:
            if dataset == None:
                return Response("No datasets found", status=404)
            ret_list.append(DatasetService.createDatasetInfoObject(dataset))
        return Response(ret_list)
    except Exception as e:
        print(e)
        return Response("Couldn't retrieve recent datasets", status=400)

"""
Fetch the first 1000 or less objects for a dataset. Create entry in cache if dataset > 1000 objects.
"""
@dataset.route("/objects/primary/<id>", methods=["GET"])
def getDatasetObjectsPrimary(id):
    filename = id + ".csv"
    fileFromS3 = s3.get_object(Bucket="agriworks-user-datasets", Key=filename)
    dataset = pd.read_csv(fileFromS3["Body"], dtype=str)
    if (len(dataset) <= 1000):
        return Response({"datasetObjects": DatasetService.buildDatasetObjectsList(dataset)})
    else:
        cacheId = str(uuid4())
        DatasetCache[cacheId] = dataset[1000:]
        return Response({"datasetObjects": DatasetService.buildDatasetObjectsList(dataset[:1000]), "cacheId": cacheId})

"""
Fetch the remaining dataset objects, 1000 or less objects at a time.
Evict cache if all dataset objects have been fetched for this session (cacheId)
"""
@dataset.route("/objects/subsequent/<cacheId>", methods=["GET"])
def getDatasetObjectsSubsequent(cacheId):
    dataset = DatasetCache[cacheId]
    if (len(dataset) <= 1000):
        del DatasetCache[cacheId]
        return Response({"datasetObjects": DatasetService.buildDatasetObjectsList(dataset)})
    else:
        DatasetCache[cacheId] = dataset[1000:]
        return Response({"datasetObjects": DatasetService.buildDatasetObjectsList(dataset[:1000]), "cacheId": cacheId})

"""
Evict dataset from cache if user exits dataset without fully reading the dataset 
(e.g remainder of dataset for that session still exists in cache)
"""
@dataset.route("/objects/evict/<cacheId>", methods=["GET"])
def evictDatasetFromCache(cacheId):
    if (cacheId in DatasetCache):
        del DatasetCache[cacheId]
        return Response(status=200)
    else:
        return Response(status=404)
