from flask import Blueprint, current_app
from Response import Response
from Models.Dataset import Dataset
from Services.DatasetService import DatasetService
import geopandas as gpd

DatasetService = DatasetService()

mapview = Blueprint("MapviewEndpoints", __name__, url_prefix="/api/mapview")
s3 = current_app.awsSession.client('s3')
DatasetCache = {}

# Mapview routes that the front end can call to get the data to show different types of maps

@mapview.route("/", methods=["GET"])
def getShapefile():
    # Returns a GeoDataFrame object
    return Response("hello world")