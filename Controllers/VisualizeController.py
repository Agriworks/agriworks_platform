import json

import requests
from flask import request
from flask_restplus import Api, Namespace, Resource, fields

from Response import Response
from Services.AuthenticationService import AuthenticationService
from Services.VisualizeService import VisualizeService

VisualizeService = VisualizeService()
visualize_ns = Namespace("visualize", "visualize methods")


@visualize_ns.route("/getFormattedData")
class GetFormattedData(Resource):
    @visualize_ns.doc(
        responses={200: "Success", 400: "Failed to generate dataset for visualization"},
        params={
            "dataset": {"in": "formData", "required": True},
            "xAxis": {"in": "formData", "required": True},
            "yAxis": {"in": "formData", "required": True},
        },
    )
    def post(self):
        dataset = json.loads(request.form["dataset"])
        xAxis = request.form["xAxis"]
        yAxis = request.form["yAxis"]
        try:
            datacollection = VisualizeService.getFormattedData(dataset, xAxis, yAxis)
        except:
            return Response("Failed to generate dataset for visualization", status=400)
        return Response({"datacollection": datacollection}, status=200)
