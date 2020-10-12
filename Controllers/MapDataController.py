from flask import Blueprint, request
from Response import Response
from flask_restplus import Api, Resource, Namespace
import geojson

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
    