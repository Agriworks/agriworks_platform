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
@auth.route("/signup", methods=["POST", "GET"])
def signup():
    if request.method == "POST":

        user = User(
            firstName=request.form["firstName"], lastName=request.form["lastName"], email=request.form["email"],
            password=request.form["password"])

        try:
            user.validate()
            # save user to database
            return "It DOES work"
        except ValidationError:
            return "error"

    else:
        return "Hello"
