from flask import Blueprint, request, make_response
from flask import current_app as app
from Services.AuthenticationService import AuthenticationService

Authentication = AuthenticationService()

admin = Blueprint("AdminController", __name__, url_prefix="/admin")

@admin.route("/", methods=["GET"])
def index():
    return {"status": "Congratulations, Agriworks is now running on your machine."}

@admin.route("/account", methods=["GET", "POST"])
@Authentication.login_required
def account():
    if request.method == "POST":
        response = make_response() #what returns

        #This is the stuff from the cookie, getting the email and password of the person who is logged in
        SID = request.cookies["SID"] #gets SID from cookie
        session = Authentication.getSession(SID) #uses SID to get session from db
        user = session["user"] #gets user from session
        sessionEmail = user["email"] #email from person logged in
        sessionPassword = user["password"] #password from person logged in

        form = request.form #the form submitted

        if form["submit"] == "email":  #might not actually be the way to do it, need to differeiante the forms

            formPassword = form["inputCurrentPassword"] #password from form

            if Authentication.saltPassword(formPassword) == sessionPassword: #make sure that the password is right
                formEmail = form["inputEmail"] #email from form
                Authentication.changeEmail(sessionEmail, formEmail)
                response.set_data("Done")
                #updated email
            else:
                response.set_data("Wrong password")
                #return an error saying that the password is not right

        if form["submit"] == "password": #doing the change password form

            formPassword = form["inputCurrentPassword"]

            if Authentication.saltPassword(formPassword) == sessionPassword:
                formNewPassword = form["inputPassword"]
                formConfirmNewPassword = form["inputConfirmPassword"]

                if formConfirmNewPassword == formNewPassword:
                    Authentication.changePassword(sessionEmail, formNewPassword)
                    response.set_data("Done")
                    #updated password
                else:
                    response.set_data("Password does not match confirm password")
                    #error password does not match confirm password
            else:
                response.set_data("Wrong password")
                #error password inputted is not correct
 
        return response
    else:
        return "This is secure content"