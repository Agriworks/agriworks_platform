from flask import Blueprint, request, make_response
from Response import Response
from Services.AuthenticationService import AuthenticationService
from Models.User import User
from Models.Session import Session
from Services.MailService import MailService
from flask import current_app as app
from mongoengine import DoesNotExist
from uuid import uuid4

import uuid

MailService = MailService()
AuthenticationService = AuthenticationService()

auth = Blueprint("AuthenticationController", __name__, url_prefix="/api/auth")

@auth.route("/login", methods=["POST"])
def login():
    session = AuthenticationService.authenticate(
        request.form["email"], request.form["password"])
    if not session:
        return Response("Incorrect username or password. Please check your credentials and try again.", status=403)
    else:
        ret = make_response("Success")
        ret.set_cookie("SID", str(session.sessionId), expires=session.dateExpires)
        return ret

@auth.route("/logout", methods=["POST"])
def logout():
    try:
        sessionId = request.form["sessionId"]
        AuthenticationService.logout(sessionId)
        return Response("Successfully logged out.", status=200)
    except:
        return Response("Unable to process request. Please reload and try again later.", status=400)


"""
Request params: first name, last name, email (will be used as username), password
Return: Success or failure codes    
"""
@auth.route("/signup", methods=["POST"])
def signup():
    user = {"firstName": request.form["firstName"],
            "lastName": request.form["lastName"],
            "email": request.form["email"],
            "password": request.form["password"],
            "organization": request.form["organization"],
            "location": request.form["location"],
            "userType": request.form["userType"]
            }

    if (not AuthenticationService.signup(user)):
        return Response("There's already an account with the provided email.", status=400)

    return Response("Signup successful", status=200)


@auth.route("/forgot-password", methods=["POST"])
def forgotPassword():
    try:
        user = AuthenticationService.getUser(email=request.form["email"])
        sessionId = uuid4()
        session = Session(user=user, sessionId=sessionId)
        session.save()
        try:
            subject = "[Agriworks] Reset password"
            html = "<p>We heard you lost your password. No worries, just click the link below to reset your password.</p><p>You can safely ignore this email if you did not request a password reset</p><br/><a href=\"http://localhost:8080/reset-password/{0}\">http://localhost:8080/reset-password/{0}</a><br/>".format(
                sessionId)
            MailService.sendMessage(user, subject, html)
            return Response("An email with instructions to reset your password has been sent to the provided email.", status=200)
        except:
            return Response("Unable to send password reset email. Please try again later.", status=400)
    except:
        return Response("No account with given email found. Please try creating a new account.", status=403)


@auth.route("/reset-password/<sessionId>", methods=["POST"])
def resetPassword(sessionId):
    try:
        if request.form["initial"]:
            user = AuthenticationService.verifySessionAndReturnUser(sessionId)
            if user != False:
                return Response(status=200)
            else:
                return Response(status=403)
    except:
        try:
            user = AuthenticationService.verifySessionAndReturnUser(sessionId)
            if user != False:
                newPassword = request.form["password"]
                AuthenticationService.changePassword(user.email, newPassword)
                return Response("Password sucessfully updated", status=200)
            else:
                return Response("Your password reset link is either invalid or is expired. Please request a new one.", status=403)
        except:
            return Response("The server could not understand your request. Please reload and try again later.", status=400)

@auth.route("/verifySession", methods=["POST"])
def verifySession():
    try:
        sessionId = request.form["sessionId"]
        if not AuthenticationService.verifySessionAndReturnUser(sessionId):
            return Response("Your session has expired. Please login again.",status=401)
        else:
            return Response(status=200)
    except DoesNotExist as e:
        return Response("Your session was not found. Please login again.",status=401)