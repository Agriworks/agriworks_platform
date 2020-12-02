from flask import Blueprint, request
from Response import Response
from Models.AgriWatchView import AgriWatchView
from Services.AgriWatchViewService import AgriWatchViewService
from Services.AuthenticationService import AuthenticationService
from flask_restplus import Resource, Namespace

AgriWatchViewService = AgriWatchViewService()
AuthenticationService = AuthenticationService()
view_ns = Namespace('view', 'view methods')

@view_ns.route('/')
class CreateNewView(Resource):
    @view_ns.doc(
        responses = {
            400: "Create new AgriWatch view error."
        },
        params = {
            'SID': {'in': 'cookies', 'required': True},
        }
    )
    def post(self):
        if ("SID" not in request.cookies):
            return Response("No session detected", status=400)
        
        view = AgriWatchViewService.createView(request)

        return Response(str(view.name))

@view_ns.route('/fetch')
class FetchViews(Resource):
    @view_ns.doc(
        responses = {
            400: "Fetch AgriWatch views error."
        },
        params = {
            'SID': {'in': 'cookies', 'required': True},
        }
    )
    def get(self):
        retList = []
        user = AuthenticationService.verifySessionAndReturnUser(request.cookies["SID"])

        views = AgriWatchView.objects.filter(author=user).order_by('-dateCreated')

        for view in views:
            if view == None:
                return Response("No views found", status=400)
            retList.append(AgriWatchViewService.createDatasetInfoObject(dataset))
        return Response(retList)