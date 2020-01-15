from flask import Blueprint, request
from Response import Response
from Services.AuthenticationService import AuthenticationService

AuthenticationService = AuthenticationService()

auth = Blueprint("AuthenticationController", __name__, url_prefix="/auth")


#TODO: Send cookies as SET-COOKIE header
@auth.route("/login", methods=["POST"])
def login():
    session = AuthenticationService.authenticate(request.form["email"], request.form["password"])
    if not session:
        return Response("Incorrect username or password", status=403)
    else:
        return {"key": "SID", "value": str(session.sessionId), "expires": session.dateExpires, "admin": session["user"]["isAdmin"]}
        

@auth.route("/logout", methods=["POST"])
def logout():
    print("Logout request received")
    sessionId = request.form["sessionId"]
    AuthenticationService.logout(sessionId)
    return Response("User logged out", status=200)

"""
Request params: first name, last name, email (will be used as username), password
Return: Success or failure codes    
"""
@auth.route("/signup", methods=["POST"])
def signup():
    user = {"firstName": request.form["firstName"], 
            "lastName": request.form["lastName"], 
            "email": request.form["email"],
            "password": request.form["password"]
            }

    if (not AuthenticationService.signup(user)):
            return Response(status=400)
    
    return Response(status=200) 