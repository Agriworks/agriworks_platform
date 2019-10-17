from flask import Blueprint
from flask import current_app as app
from Services.AuthenticationService import Authentication

AuthenticationService = Authentication()

auth = Blueprint("AuthenticationEndpoints", __name__, "/auth")

@auth.route("/login", methods=["POST"])
def authenticateUser():
    if not AuthenticationService.authenticate(request.form.email, request.form.password):
        return "Incorrect username or password"
    else:
        return "Authentication"
"""
TODO: KOAH
Create signup API endpoint
Request params: first name, last name, email (will be used as username), password
Return: Success or failure codes    
"""