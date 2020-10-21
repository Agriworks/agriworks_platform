from flask import Blueprint, request, current_app, send_file, jsonify
from Response import Response
from flask_restplus import Api, Resource, Namespace
import geojson
import json
import gzip


map_data_ns = Namespace('map_data', 'geojson map data')

s3 = current_app.awsSession.client('s3')

@map_data_ns.route('/')
class MapDataAPI(Resource):
    @map_data_ns.doc(
        responses={
            400: "No session detected", 
            400: "Prohibited level type",
            400: "Empty fields detected. Please remove empty values from your dataset and try again." 
        },
        params={
            'level': 'administrative level',
        }
    )
    def get(self):
        accepted_levels = [str(level) for level in range(1,5)]
        level = request.args["level"]
        if level not in accepted_levels:
            return Response("Prohibited level type", status=400)
        file_name = f"IND_adm{level}.geojson"
        file_from_s3 = s3.get_object(Bucket="agriworks-map-geometry", Key=file_name)
        file_content = file_from_s3["Body"].read()
        data = json.loads(file_content)
        
        return Response(data)
    