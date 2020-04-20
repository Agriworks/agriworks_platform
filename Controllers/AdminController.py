from flask import Blueprint, request
from flask import current_app as app
from Services.AuthenticationService import AuthenticationService
from Response import Response

Authentication = AuthenticationService()

admin = Blueprint("AdminController", __name__, url_prefix="/api/admin")

@admin.route("/", methods=["GET"])
def index():
    return {"status": "Congratulations, Agriworks is now running on your machine."}

@admin.route("/account", methods=["POST"])
@Authentication.login_required
def account():

    form = request.form #the form submitted

    #This is the stuff from the cookie, getting the email and password of the person who is logged in
    SID = form["sessionID"] #gets SID from cookie
    session = Authentication.getSession(SID) #uses SID to get session from db
    user = session["user"] #gets user from session
    sessionEmail = user["email"] #email from person logged in
    sessionPassword = user["password"] #password from person logged in
    
    if form["submit"] == "email":  #might not actually be the way to do it, need to differeiante the forms

        formPassword = form["inputCurrentPassword"] #password from form

        if Authentication.saltPassword(formPassword) == sessionPassword: #make sure that the password is right
            formEmail = form["inputEmail"] #email from form


            #Check to see if the email is already in use
            if not Authentication.emailIsAlreadyInUse(formEmail):
                Authentication.changeEmail(sessionEmail, formEmail)
                return Response("Email Updated", status=200)
                #updated email
            else:
                #Email is already in use
                return Response("Email is already in use", status=400)
        else:
            return Response("Wrong password", status=400)
            #return an error saying that the password is not right

    elif form["submit"] == "password": #doing the change password form

        formPassword = form["inputCurrentPassword"]

        if Authentication.saltPassword(formPassword) == sessionPassword:
            formNewPassword = form["inputPassword"]
            formConfirmNewPassword = form["inputConfirmPassword"]

            if formConfirmNewPassword == formNewPassword:
                Authentication.changePassword(sessionEmail, formNewPassword)
                return Response("Updated Password", status=200)
                #updated password
            else:
                return Response("Password does not match confirm password", status=400)
                #error password does not match confirm password
        else:
            return Response("Wrong password", status=400)
            #error password inputted is not correct

    return Response("No form submitted", status=400)