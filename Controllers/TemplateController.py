from flask import Blueprint, request, current_app
from Response import Response
from mongoengine.queryset.visitor import Q
from Models.Template import Template
from Services.TemplateService import TemplateService
from Services.AuthenticationService import AuthenticationService
from Models.User import User

TemplateService = TemplateService()
AuthenticationService = AuthenticationService()

template = Blueprint("TemplateController", __name__, url_prefix="/api/templates")

#Used to delete a template
@template.route("/delete/<templateName>", methods=["DELETE"])
def deleteDataset(templateName):
    user = AuthenticationService.verifySessionAndReturnUser(
        request.cookies["SID"])
    template = Template.objects.get(templateName=templateName)

    if template == None:
        return Response("Unable to retrieve template information. Template does not exist.", status=400)
    if (template.author != user):
        return Response("You do not have permission to delete that template.", status=403)

    try: 
        template.delete()
        return Response("Succesfully deleted dataset.", status=200)
    except:
        return Response("Unable to delete dataset.", status=500)

#Used to retrieve a template
@template.route("/<templateName>", methods=["GET"])
def getTemplate(templateName):
    
    template = Template.objects.get(templateName=templateName)

    if template == None:
        return Response("No template with name " + templateName + " found", status=400)
    else:
        return Response(TemplateService.getTemplate(template))

#Used to store a template
@template.route("/create", methods=["POST"])
def create():
    return Response("New template successfully stored") if TemplateService.createTemplate(request) else Response("Unable to create new template")