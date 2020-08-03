from flask import Flask, request, jsonify, make_response   
from functools import wraps
from Response import Response
from Services.AuthenticationService import AuthenticationService 
AuthenticationService = AuthenticationService()


NON_PROTECTED_ENDPOINTS = ["index", "sendStaticComponent", "AdminController.index", "AuthenticationController.login", "AuthenticationController.signup", "AuthenticationController.confirmUser", "AuthenticationController.forgotPassword", "AuthenticationController.resendConfirmationEmail", "AuthenticationController.resetPassword", "AuthenticationController.verifySession"]

def authRequired(f):  
    @wraps(f)  
    def decorator(*args, **kwargs):
        if "SID" not in request.cookies:
            return Response(status=403)

        cookie = request.cookies["SID"]
        
        try:
            user = AuthenticationService.verifySessionAndReturnUser(cookie)
            return f(*args, **kwargs)
        except:
            return Response("Invalid session ID", status=403)

    return decorator

