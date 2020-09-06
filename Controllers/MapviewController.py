from flask import Blueprint, current_app
from Response import Response
from Models.Dataset import Dataset
from Services.DatasetService import DatasetService
import geopandas as gpd
import json

DatasetService = DatasetService()

mapview = Blueprint("MapviewEndpoints", __name__, url_prefix="/api/mapview")
s3 = current_app.awsSession.client('s3')
DatasetCache = {}

# Mapview routes that the front end can call to show different types of maps
@mapview.route("/getGeometry", methods=["GET"])
def getGeometry():
    # Returns a JSON object
    print("attept to open file")
    with open("/Users/cody/Hack4Impact/agriworks_platform/IND_adm1.json") as file:
        data = json.load(file)

    print("loaded geometry")
    return Response(data)