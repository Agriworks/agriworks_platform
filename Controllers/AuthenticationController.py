from flask import Blueprint, request
from Response import Response
from Services.AuthenticationService import AuthenticationService
from Models.User import User
from Models.Session import Session
from flask import current_app as app
from flask_mail import Mail, Message


mail = Mail(app)
AuthenticationService = AuthenticationService()

auth = Blueprint("AuthenticationController", __name__, url_prefix="/auth")


# TODO: Send cookies as SET-COOKIE header
@auth.route("/login", methods=["POST"])
def login():
    session = AuthenticationService.authenticate(
        request.form["email"], request.form["password"])
    if not session:
        return Response("Incorrect username or password. Please check your credentials and try again.", status=403)
    else:
        return {"key": "SID", "value": str(session.sessionId), "expires": session.dateExpires, "admin": session["user"]["isAdmin"]}


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
            "password": request.form["password"]
            }

    if (not AuthenticationService.signup(user)):
        return Response("There's already an account with the provided email.", status=400)

    return Response("Signup successful", status=200)


@auth.route("/forgot-password", methods=["POST"])
def forgotPassword():
    try:
        userObject = User.objects.get(email=request.form["email"])
        session = Session(user=userObject)
        session.save()
        try:
            subject = "[Agriworks] Reset password"
            html = "<p>Hi there,</p><p>We heard you lost your password. No worries, just click the link below to reset your password.</p><p>You can safely ignore this email if you did not request a password reset</p><br/><a href=\"http://localhost:8080/reset-password/{0}\">http://localhost:8080/reset-password/{0}</a><br/><p>Thanks,</p><p>Agriworks Team</p>".format(
                session.sessionId)
            msg = Message(recipients=[userObject.email],
                          subject=subject, html=html)
            mail.send(msg)
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
