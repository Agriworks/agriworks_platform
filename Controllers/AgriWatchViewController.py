from flask import Blueprint, request
from flask_restplus import Namespace, Resource

from Models.AgriWatchView import AgriWatchView
from Response import Response
from Services.AgriWatchViewService import AgriWatchViewService
from Services.AuthenticationService import AuthenticationService

AgriWatchViewService = AgriWatchViewService()
AuthenticationService = AuthenticationService()
view_ns = Namespace("view", "view methods")


@view_ns.route("/create")
class CreateNewView(Resource):
    @view_ns.doc(
        responses={400: "Create new AgriWatch view error."},
        params={
            "SID": {"in": "cookies", "required": True},
        },
    )
    def post(self):
        if "SID" not in request.cookies:
            return Response("No session detected", status=400)

        view = AgriWatchViewService.createView(request)

        return Response(str(view.dataset) + str(view.visualType))


@view_ns.route("/fetch")
class FetchViews(Resource):
    @view_ns.doc(
        responses={400: "Error fetching AgriWatch views."},
        params={
            "SID": {"in": "cookies", "required": True},
        },
    )
    def get(self):
        retList = []
        user = AuthenticationService.verifySessionAndReturnUser(request.cookies["SID"])

        views = AgriWatchView.objects.filter(author=user).order_by("-dateCreated")

        for view in views:
            if view == None:
                return Response("No views found", status=400)
            retList.append(AgriWatchViewService.makeViewObject(view))
        return Response(retList)
