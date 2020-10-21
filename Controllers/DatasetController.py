from flask import Blueprint, request, current_app
from Response import Response
from mongoengine.queryset.visitor import Q
from Models.Dataset import Dataset
from Services.DatasetService import DatasetService
from Services.AuthenticationService import AuthenticationService
from Models.User import User
import boto3
import botocore
import pandas as pd
from uuid import uuid4
from flask_restplus import Api, Resource, Namespace


DatasetService = DatasetService()
AuthenticationService = AuthenticationService()
dataset_ns = Namespace('dataset', 'upload methods')

s3 = current_app.awsSession.client('s3')
DatasetCache = {}



@dataset_ns.route("/list/<pageNumber>")
class Get(Resource):
    @dataset_ns.doc(
        responses={
            400: "No datasets matching the query were found"
        },
        params={
            'SID': {'in': 'cookies', 'required': True},
        }
    ) 
    def get(self, pageNumber):
        retList = []
        datasets = []

        user = AuthenticationService.verifySessionAndReturnUser(
            request.cookies["SID"])

        allDatasets = Dataset.objects.filter( Q(public=True) | Q(author=user)).order_by('-dateCreated')

        if pageNumber == "all":
            datasets = allDatasets
        elif pageNumber == "0":
            datasets =  allDatasets[:16]
        else:
            datasetIndex = 16 + 12 * (int(pageNumber) - 1)
            datasets =  allDatasets[datasetIndex: datasetIndex + 12]

        if len(datasets) == 0:
            return Response("No datasets matching the query were found", status=400)

        for dataset in datasets:
            retList.append(DatasetService.createDatasetInfoObject(dataset))

        return Response(retList)

@dataset_ns.route("/metadata/<datasetId>")
class GetDataset(Resource):
    @dataset_ns.doc(
        responses={
            400: "Unable to retrieve dataset information. Please try again later.", 
            403: "You do not have permission to access that dataset."
        },
        params={
            'SID': {'in': 'cookies', 'required': True},
        }
    ) 
    def get(self, datasetId): 
        user = AuthenticationService.verifySessionAndReturnUser(
            request.cookies["SID"])
        dataset = Dataset.objects.get(id=datasetId)

        if dataset == None:
            return Response("Unable to retrieve dataset information. Please try again later.", status=400)
        if (dataset.public == False and dataset.author != user):
            return Response("You do not have permission to access that dataset.", status=403)
        
        Dataset.objects(id=datasetId).update_one(inc__views=1)
        AuthenticationService.updateRecentDatasets(request.cookies["SID"],datasetId)
        return Response(DatasetService.createDatasetInfoObject(dataset, withHeaders=True))

@dataset_ns.route("/columndata/<datasetId>")
class GetColumnData(Resource):
    @dataset_ns.doc(
        responses={
            400: "Unable to retrieve dataset information. Please try again later.", 
            403: "You do not have permission to access that dataset."
        },
        params={
            'SID': {'in': 'cookies', 'required': True},
        }
    )
    def get(self,datasetId):
        user = AuthenticationService.verifySessionAndReturnUser(
            request.cookies["SID"])
        dataset = Dataset.objects.get(id=datasetId)

        if dataset == None:
            return Response("Unable to retrieve dataset information. Please try again later.", status=400)
        if (dataset.public == False and dataset.author != user):
            return Response("You do not have permission to access that dataset.", status=403)

        columnData = DatasetService.getColumnData(dataset)
        
        return Response(columnData)

        

@dataset_ns.route("/objects/primary/<dataset_id>")
class GetDatasetObjectsPrimary(Resource):
    @dataset_ns.doc(
        responses={
            403: "You do not have access to that dataset."
        },
        params={
            'SID': {'in': 'cookies', 'required': True},
        }
    )  
    def get(self, dataset_id):
        """ Fetch the first 1000 or less objects for a dataset and create entry in cache if dataset > 1000 objects. """ 
        user = AuthenticationService.verifySessionAndReturnUser(
            request.cookies["SID"])

        if (Dataset.objects.get(Q(id=dataset_id) & (Q(public=True) | Q(author=user) ) ) != None):
            filename = dataset_id + ".csv"
            fileFromS3 = s3.get_object(Bucket="agriworks-user-datasets", Key=filename)
            dataset = pd.read_csv(fileFromS3["Body"], dtype=str)
        else:
            return Response("You do not have access to that dataset.", status=403)

        if (len(dataset) <= 1000):
            return Response({"datasetObjects": DatasetService.buildDatasetObjectsList(dataset)})
        else:
            cacheId = str(uuid4())
            DatasetCache[cacheId] = dataset[1000:]
            return Response({"datasetObjects": DatasetService.buildDatasetObjectsList(dataset[:1000]), "cacheId": cacheId})


@dataset_ns.route("/objects/subsequent/<cacheId>")
class GetDatasetObjectsSubsequent(Resource):
    def get(self, cacheId):
        """
        Fetch the remaining dataset objects, 1000 or less objects at a time, evict cache if all dataset objects have been fetched for this session (cacheId)
        """  
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
@dataset_ns.route("/objects/evict/<cacheId>")
class EvictDatasetFromCache(Resource): 
    def get(self, cacheId): 
        if (cacheId in DatasetCache):
            del DatasetCache[cacheId]
            return Response(status=200)
        else:
            return Response(status=404)



# TODO: Get any type of file, not just csv. May just need to encode the files without filename. But then need to determine what content_type the file is
@dataset_ns.route('/download/<id>')
class File(Resource): 
    def get(self, id): 
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

@dataset_ns.route("/<datasetId>")
class DeleteDataset(Resource):
    @dataset_ns.doc(
        responses={
            200: "Succesfully deleted dataset.", 
            400: "Unable to retrieve dataset information. Please try again later.", 
            403: "You do not have access to that dataset.", 
            500: "Unable to delete dataset."
        },
        params={
            'SID': {'in': 'cookies', 'required': True},
        }
    ) 
    def delete(self, datasetId): 
        user = AuthenticationService.verifySessionAndReturnUser(
            request.cookies["SID"])
        dataset = Dataset.objects.get(id=datasetId)

        if dataset == None:
            return Response("Unable to retrieve dataset information. Please try again later.", status=400)
        if (dataset.author != user):
            return Response("You do not have permission to delete that dataset.", status=403)

        try: 
            s3.delete_object(Bucket="agriworks-user-datasets", Key=datasetId + ".csv")
            dataset.delete()
            return Response("Succesfully deleted dataset.", status=200)
        except:
            return Response("Unable to delete dataset.", status=500)


@dataset_ns.route("/search/<searchQuery>")
class Search(Resource):
    @dataset_ns.doc(
        responses={
            400: "Error processing request. Please try again later.", 
            400: "Unable to retrieve datasets with the given search parameter.", 
        },
        params={
            'SID': {'in': 'cookies', 'required': True},
        }
    )  
    def get(self, searchQuery): 
        datasets = []
        browseURL = "browse"
        manageURL = "manage"
        referrerURL = request.headers["referer"].split('/')[-1]

        matchedDatasets = []
        typeUser = None

        user = AuthenticationService.verifySessionAndReturnUser(
                        request.cookies["SID"])

        try:
            if searchQuery == "" or searchQuery == " ":
                raise
            else:
                #Perform search only on user datasets
                if referrerURL == manageURL:
                    userDatasets = Dataset.objects.filter(author=user)
                    matchedDatasets = userDatasets.search_text(
                        searchQuery).order_by('$text_score')
                    typeUser = True
                #Perform search on all datasets
                elif referrerURL == browseURL:
                    visibleDatasetsToUser = Dataset.objects.filter(Q(author=user) | Q(public=True))
                    matchedDatasets = visibleDatasetsToUser.search_text(
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

@dataset_ns.route("/user/")
class GetUsersDatasets(Resource):
    @dataset_ns.doc(
        responses={
            400: "No datasets found", 
        },
        params={
            'SID': {'in': 'cookies', 'required': True},
        }
    )  
    def get(self): 
        retList = []
        user = AuthenticationService.verifySessionAndReturnUser(
            request.cookies["SID"])
        datasets = Dataset.objects.filter(author=user).order_by('-dateCreated')
        for dataset in datasets:
            if dataset == None:
                return Response("No datasets found", status=400)
            retList.append(DatasetService.createDatasetInfoObject(dataset))
        return Response(retList)

@dataset_ns.route("/popular/")
class Popular(Resource):
    @dataset_ns.doc(
        responses={
            400: "No datasets found",
            400: "Couldn't retrieve popular datasets" 
        },
        params={
            'SID': {'in': 'cookies', 'required': True},
        }
    ) 
    def get(self): 
        try: 
            retList = []
            user = AuthenticationService.verifySessionAndReturnUser(request.cookies["SID"])
            # sorts the datasets by ascending order
            datasets = Dataset.objects.filter(Q(author=user) | Q(public=True)).order_by("-views")[:5]
            for dataset in datasets:
                if dataset == None:
                    return Response("No datasets found", status=400)
                retList.append(DatasetService.createDatasetInfoObject(dataset))
            return Response(retList)
        except:
            return Response("Couldn't retrieve popular datasets", status=400)

@dataset_ns.route("/recent/")
class Recent(Resource):
    @dataset_ns.doc(
        responses={
            400: "Couldn't retrieve recent datasets"        
        },
        params={
            'SID': {'in': 'cookies', 'required': True},
        }
    ) 
    def get(self): 
        try: 
            retList = []
            # use cookies to retrieve user
            user = AuthenticationService.verifySessionAndReturnUser(
                request.cookies["SID"])
            recentDatasetIds = user.recentDatasets[:5]
            # retrieve the actual datasets from these ids
            for datasetId in recentDatasetIds:
                try:
                    retList.append(DatasetService.createDatasetInfoObject(
                        Dataset.objects.get(id=datasetId)))
                except:
                    continue
            return Response(retList)

        except Exception as e:
            return Response("Couldn't retrieve recent datasets", status=400)

@dataset_ns.route("/new/")
class New(Resource):
    @dataset_ns.doc(
        responses={
            400: "Couldn't retrieve recent datasets", 
            404: "No datasets found"       
        },
        params={
            'SID': {'in': 'cookies', 'required': True},
        }
    )  
    def get(self): 
        try: 
            retList = []
            user = AuthenticationService.verifySessionAndReturnUser(
                request.cookies["SID"])
            # get users datasets by date created and sort by descending order
            newDatasets = Dataset.objects(author=user).order_by("-dateCreated")[:5]
            for dataset in newDatasets:
                if dataset == None:
                    return Response("No datasets found", status=404)
                retList.append(DatasetService.createDatasetInfoObject(dataset))
            return Response(retList)
        except Exception as e:
            print(e)
            return Response("Couldn't retrieve recent datasets", status=400)
