from flask import Flask, request, jsonify, make_response   
from functools import wraps
from Response import Response
from Services.AuthenticationService import AuthenticationService 
auth = AuthenticationService()

def authRequired(f):  
    @wraps(f)  
    def decorator(*args, **kwargs):
        cookie = None
        if "SID" in request.cookies:
            cookie = request.cookies["SID"]
        
        if not cookie:
            return Response("No cookie present", status=403)

        try:
            user = auth.verifySessionAndReturnUser(cookie)
        except:
            return Response("Invalid session ID", status=403)
        if user:
            return f(*args, **kwargs)
    return decorator

