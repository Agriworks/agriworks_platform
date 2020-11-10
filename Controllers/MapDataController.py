from flask import Blueprint, request, jsonify
from Response import Response
from flask_restplus import Api, Resource, Namespace
import json
from Services.MapDataService import MapDataService



MapDataService = MapDataService()
map_data_ns = Namespace('map_data', 'geojson map data')

@map_data_ns.route('/')
class MapDataAPI(Resource):
    @map_data_ns.doc(
        responses={
            400: "No session detected", 
            400: "Prohibited file type",
            400: "Empty fields detected. Please remove empty values from your dataset and try again." 
        },
        params={
            'level': 'administrative level',
        }
    )
    def get(self):
        # with open('GeoJSON/IND_adm0.geojson') as f:
        #     gj = geojson.load(f)
        # features = gj['features']
        return Response('MAP DATA API')


@map_data_ns.route("/getMap")
class GetMap(Resource):
    @map_data_ns.doc(
        repsonses={
            200: "Success",
            400: "Failed to generate map"
        },
        params={
            
        }
    )
    def post(self):
        print("In the method")
        dataset = json.loads(request.form['dataset'])
        columnLabels = request.form['columnLabels']
        locationCol = request.form['locationCol']
        dataCol1 = request.form['dataCol1']
        dataCol2 = request.form['dataCol2'] 
        # print("ColumnLabels")
        # print(columnLabels)
        # print(type(columnLabels))
        columnLabels = json.loads(columnLabels)
        # print("Trying something")
        # print("Dataset")
        # print(type(dataset))
        try:
            heatMap, colors, bucketGrades = MapDataService.map(dataset, columnLabels, locationCol, dataCol1, dataCol2)
        except:
            return Response("Failed to generate map", status=400)

        return Response({"data": heatMap, "colors": colors, "bucketGrades": bucketGrades}, status= 200)

    