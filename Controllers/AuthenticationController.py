from flask import Blueprint, request, Response, jsonify
from mongoengine import ValidationError
from flask import current_app as app
from Services.AuthenticationService import AuthenticationService
from Models.User import User
AuthenticationService = AuthenticationService()

auth = Blueprint("AuthenticationController", __name__, url_prefix="/auth")


@auth.route("/login", methods=["POST"])
def login():
    if not AuthenticationService.authenticate(request.form["email"], request.form["password"]):
        return "Incorrect username or password"
    else:
        return "Authentication"


"""
TODO: KOAH
Create signup API endpoint
Request params: first name, last name, email (will be used as username), password
Return: Success or failure codes    
"""

