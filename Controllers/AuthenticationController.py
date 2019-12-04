from flask import Blueprint, request, Response, make_response, jsonify, abort
from mongoengine import ValidationError
from flask import current_app as app
from Services.AuthenticationService import AuthenticationService
from Models.User import User
from datetime import timedelta
AuthenticationService = AuthenticationService()

auth = Blueprint("AuthenticationController", __name__, url_prefix="/auth")


@auth.route("/login", methods=["POST"])
def login():
    print("Request data is")
    print(request.form)
    auth = AuthenticationService.authenticate(request.form["email"], request.form["password"])
    #auth = False
    if not auth:
        print("This login is not authorized! 403 error code sent to be interpreted by fe!")
        abort(403, {"message": "Incorrect username or password"})
        print("This was not authorized!")
        #return {"status": "Incorrect username or password"}
    else:
        change = timedelta(days=30)
        expires = auth.date_created + change
        print("Session id:", str(auth.sessionId))
        response = {"key": "SID", "value": str(auth.sessionId), "expires": expires}
        return response
"""
Request params: first name, last name, email (will be used as username), password
Return: Success or failure codes    
"""
@auth.route("/signup", methods=["GET","POST"])
def signup():
    if request.method == "POST":
        user = {"firstName": request.form["firstName"], 
                "lastName": request.form["lastName"], 
                "email": request.form["email"],
                "password": request.form["password"]}
        success,error = AuthenticationService.signup(user)  # Authenticate signup route
        if not success:
            if error=="DuplicateError":
                #Do something
            else: #Must be TypeError
                #Do something else
            return error
        return "Placeholder POST"  # redirect if successful
    return "Placeholder GET"  # render template of signup page for Get
