from flask import Blueprint, request, Response
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
        """
        add cookie to response object
        return response 
        """
        return "Authentication"
"""
TODO: KOAH
Create signup API endpoint
Request params: first name, last name, email (will be used as username), password
Return: Success or failure codes    
"""
@auth.route("/signup", methods=["POST"])
def signup():
    if request.method == "POST":
        # document = {"firstName": request.form["firstName"],
        #             "lastName": request.form["lastName"],
        #             "email": request.form["email"],
        #             "password": request.form["password"]
        #             }
        # doc = Document(values=document)
        user = User(
            firstName=request.form["firstName"], lastName=request.form["lastName"], email=request.form["email"],
            password=request.form["password"])
        # try:
        # if user.validate():
        # save user to database
        # try:
        if user.validate() != "":
            return "It DOES work"
        # except:
        #     return "error"

    else:
        return "Hello"