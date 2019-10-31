from flask import Blueprint, request, Response, make_response
from flask import current_app as app
from Services.AuthenticationService import AuthenticationService
from Models.User import User
from datetime import timedelta
AuthenticationService = AuthenticationService()

auth = Blueprint("AuthenticationController", __name__, url_prefix="/auth")

@auth.route("/login", methods=["POST"])
def login():
    auth = AuthenticationService.authenticate(request.form["email"], request.form["password"])
    if not auth:
        return "Incorrect username or password"
    else:
        response = make_response()
        change = timedelta(days=30)
        expries = auth.date_created + change
        response.set_cookie(key="SID", value=str(auth.sessionId), expires=expries)
        response.set_data("logged in")
        """
        add cookie to response object
        return response 
        """
        return response
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
        #             "password": request.form["password"
        #             }s
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