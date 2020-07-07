from flask import Blueprint
from flask import current_app as app 
from flask import request, redirect, url_for
from functools import wraps
from uuid import uuid4
from Models.User import User
from Models.Session import Session 
from datetime import datetime
from Models.Template import Template
import json 

class TemplateService():
    
    def __init__(self):
        return

    """ 
    Return the template
    """ 
    def getTemplate(self, **kwargs):
        if not Template.objects(**kwargs):
            return False

        template = Template.objects.get(**kwargs) #use objects.get to retreive one result
        
        return template

    
    """
    Save the user to the database upon signup if they don't exist
    """
    def save(self, template): 
        if self.getTemplate(templateName=template.templateName): 
            return False
        else:
            template.save()
            return True
          
    """
    Currently, all users will not be administrators.
    """
    def createTemplate(self, document):
        template = Template(
            templateName=document["name"],
            author=document["author"],
            headers=json.loads(document["headers"])
            )

        template.validate()  # TODO: enclose this in a try/catch block /check if its an error with the type entered

        if (self.save(template)):
            return True
        else:
            return False

    def templateNameIsAlreadyInUse(self, templateName):
        return Template.objects(templateName=templateName)
    
    def changeTemplateName(self, oldTemplateName, newTemplateName):
        Template.objects.get(templateName=oldTemplateName).update(templateName=newTemplateName)

    def changeHeaders(self, templateName, headers):
        Template.objects.get(templateName=templateName).update(headers=headers)   