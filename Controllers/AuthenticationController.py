from flask import Blueprint, request, Response, make_response, jsonify
from mongoengine import ValidationError
from flask import current_app as app
from Services.AuthenticationService import AuthenticationService
from Models.User import User
from datetime import timedelta
AuthenticationService = AuthenticationService()

auth = Blueprint("AuthenticationController", __name__, url_prefix="/auth")


@auth.route("/login", methods=["POST"])
def login():
    auth = AuthenticationService.authenticate(request.form["email"], request.form["password"])
    #auth = False
    if not auth:
        print("This login is not authorized! 403 forbidden")
        return Response({"message": "Incorrect username or password"}, status=403)
    else:
        change = timedelta(days=30)
        expires = auth.date_created + change
        
        session = AuthenticationService.getSession(auth.sessionId) # gets session from db
        user = session["user"] #gets user from session
        sessionAdmin = user["admin"] #boolean to determine whether a user is an admin or not

        print("Session id:", str(auth.sessionId))
        response = {"key": "SID", "value": str(auth.sessionId), "expires": expires, "admin": sessionAdmin}
        return response

@auth.route("/logout", methods=["POST"])
def logout():
    print("Logout request received")
    sessionId = request.form["sessionId"]
    AuthenticationService.logout(sessionId)
    return {"status": "User logged out"}

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
                return Response({"message": "Duplicate error"}, status=400)
            else: #Must be TypeError
                #Do something else
                return Response({"message": "Type error"}, status=400)
        return "Placeholder POST"  # redirect if successful
    return "Placeholder GET"  # render template of signup page for Get
