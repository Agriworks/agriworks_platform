from flask import Blueprint, request, make_response, url_for, redirect
from flask import current_app as app
from Response import Response
from Services.AuthenticationService import AuthenticationService
from Models.User import User
from Models.Dataset import Dataset
from Models.Session import Session
from Services.MailService import MailService
from mongoengine import DoesNotExist
from uuid import uuid4
import google.oauth2.credentials
import requests


from flask_restplus import Api, Resource, fields, Namespace

MailService = MailService()
AuthenticationService = AuthenticationService()
auth_ns = Namespace('auth', 'Auth methods')


@auth_ns.route("/authorize")
class Authorize(Resource):
    @auth_ns.doc(
        responses={
            200: "Success",
            403: "Email already registered with our service"
        },
        params={
            'redirect_uri': {'in': 'formData', 'required': True},
            'authCode': {'in': 'formData', 'required': True}
        }
    )
    def post(self):
        flow = app.flow
        flow.redirect_uri = request.form["redirect_uri"]
        authCode = request.form["code"]
        flow.fetch_token(code=authCode)

        credentials = flow.credentials
        req_url = "https://www.googleapis.com/oauth2/v1/userinfo?access_token=" + credentials.token
        user_info = requests.get(req_url).json()

        user = AuthenticationService.getUser(email=user_info['email'])

        if user:
            if not user.password:
                sessionId = uuid4()
                session = Session(user=user, sessionId=sessionId)
                session.save()
                ret = make_response(user_info)
                ret.set_cookie("SID", str(session.sessionId),
                            expires=session.dateExpires)
                return ret
            return Response("Email already registered with our service", status=403)
        else:
            ret = {}
            ret['message'] = "Redirect to complete sign up"
            ret['user'] = user_info
            return Response(ret, status=200)


@auth_ns.route("/login")
class Login(Resource):
    @auth_ns.doc(
        responses={
            200: "Success", 
            401: "Incorrect username or password. Please check your credentials and try again.", 
            403: "You must confirm your account to log in."
        },
        params={
            'email': {'in': 'formData', 'required': True},
            'password': {'in': 'formData', 'required': True}
        }
    )
    def post(self):
        session = AuthenticationService.authenticate(request.form["email"], request.form["password"])
        if not session:
            return Response("Incorrect username or password. Please check your credentials and try again.", status=401)
        
        user = User.objects.get(email=request.form["email"])
        if not AuthenticationService.isUserConfirmed(user):
            return Response("You must confirm your account to log in.", status=403)
        
        ret = make_response("Success")
        ret.set_cookie("SID", str(session.sessionId), expires=session.dateExpires)
        return ret

@auth_ns.route("/logout")
class Logout(Resource):
    @auth_ns.doc(
        responses={
            200: "Successfully logged out.", 
            400: "Unable to process request. Please reload and try again later."            
        },
        params={
            'sessionId': {'in': 'formData', 'required': True},
        }
    )
    def post(self): 
        try:
            sessionId = request.form["sessionId"]
            AuthenticationService.logout(sessionId)
            return Response("Successfully logged out.", status=200)
        except:
            return Response("Unable to process request. Please reload and try again later.", status=400)

@auth_ns.route("/signup")
class Signup(Resource):
    @auth_ns.doc(
        responses={
            200: "Signup successful", 
            400: "There's already an account with the provided email.",
            403: "Signup unsuccessful. Please try again."
        },
        params={
            'firstName': {'in': 'formData', 'required': True},
            'lastName': {'in': 'formData', 'required': True},
            'email': {'in': 'formData', 'required': True},
            'password': {'in': 'formData', 'required': True},
            'organization': {'in': 'formData', 'required': True},
            'location': {'in': 'formData', 'required': True},
            'userType': {'in': 'formData', 'required': True}
        }
    ) 
    def post(self): 
        user = {"firstName": request.form["firstName"],
                "lastName": request.form["lastName"],
                "email": request.form["email"],
                "password": request.form["password"],
                "organization": request.form["organization"],
                "location": request.form["location"],
                "userType": request.form["userType"]
                }

        try:
            User.objects.get(email=user["email"])
            return Response("There's already an account with the provided email.", status=400)
        except:
            try:
                AuthenticationService.signup(user)
                userConfirmationId = uuid4()
                user = User.objects.get(email=user["email"])
                if AuthenticationService.isUserConfirmed(user):
                    sessionId = uuid4()
                    session = Session(user=user, sessionId=sessionId)
                    session.save()
                    data = {"message": "Google authorized successful!",
                            "user": user.email}
                    ret = make_response(data)
                    ret.set_cookie("SID", str(session.sessionId),
                                expires=session.dateExpires)
                    return ret
                AuthenticationService.setUserConfirmationId(user, userConfirmationId)
                sub = "Confirm Account"
                msg = f"<p>Congratulations, you've registered for Agriworks. Please click the link below to confirm your account.</p><p><a href=\"{app.rootUrl}/confirm-user/{userConfirmationId}\"> Confirm account </a></p>"
                MailService.sendMessage(user, sub, msg)
                return Response("Signup successful", status=200)
            except:
                return Response("Signup unsuccessful. Please try again.", status=403)

@auth_ns.route("/resend-confirmation-email/<email>")
class ResendConfirmationEmail(Resource):
    @auth_ns.doc(
        responses={
            200: "New confirmation email sent.",
            400: "There's already an account with the provided email.",
            403: "Resend confirmation email unsuccessful."
        },
    )  
    def post(self, email): 
        try:
            user = User.objects.get(email=email)
            if user.isConfirmed:
                return Response("User already confirmed.",status=403)
            newUserConfirmationId = uuid4()
            AuthenticationService.setUserConfirmationId(user, newUserConfirmationId)
            sub = "Confirm Account"
            msg = f"<p>Congratulations, you've registered for Agriworks. Please click the link below to confirm your account.</p><p><a href=\"{app.rootUrl}/confirm-user/{newUserConfirmationId}\"> Confirm account </a></p>"
            MailService.sendMessage(user, sub, msg)
            return Response("New confirmation email sent.", status=200)
        except:
            return Response("Resend confirmation email unsuccessful.", status=403)

@auth_ns.route("/confirm-user/<userConfirmationId>")
class ConfirmUser(Resource):
    @auth_ns.doc(
        responses={
            200: "Account confirmed successfully. You may now login.",
            404: "No account was found using the provided confirmation code."
        },
    ) 
    def post(self, userConfirmationId): 
        try:
            user = User.objects.get(confirmationId=userConfirmationId)
            AuthenticationService.setUserAsConfirmed(user)
            return Response("Account confirmed successfully. You may now login.")
        except:
            return Response("No account was found using the provided confirmation code.", status=404)

@auth_ns.route("/forgot-password")
class ForgotPassword(Resource): 
    @auth_ns.doc(
        responses={
            200: "An email with instructions to reset your password has been sent to the provided email.",
            400: "Unable to send password reset email. Please try again later.",
            403: "No account with given email found. Please try creating a new account."
        },
        params={
            'email': {'in': 'formData', 'required': True},
        }
    ) 
    def post(self): 
        try:
            user = AuthenticationService.getUser(email=request.form["email"])
            passwordResetId = uuid4()
            AuthenticationService.setUserResetID(user, passwordResetId)
            try:
                subject = "Reset Password"
                html = f"<p>We heard you lost your password. No worries, just click the link below to reset your password.</p><p>You can safely ignore this email if you did not request a password reset</p><br/><a href=\"{app.rootUrl}/reset-password/{passwordResetId}\"> Reset password </a><br/>"
                MailService.sendMessage(user, subject, html)
                return Response("An email with instructions to reset your password has been sent to the provided email.", status=200)
            except:
                return Response("Unable to send password reset email. Please try again later.", status=400)
        except:
            return Response("No account with given email found. Please try creating a new account.", status=403)

@auth_ns.route("/reset-password/<passwordResetId>")
class ResetPassword(Resource): 
    @auth_ns.doc(
        responses={
            200: "Password sucessfully updated",
            400: "Please provide a new password.",
            403: "Password and Confirm Password fields must be the same", 
            403: "Please choose a password that you haven't used before",  
            403: "Your password reset link is either invalid or expired. Please request a new one."
        },
        params={
            'password': {'in': 'formData', 'required': True},
            'confirmPassword': {'in': 'formData', 'required': True},
        }
    ) 
    def post(self, passwordResetId):     
        try:
            user = AuthenticationService.checkUserResetID(passwordResetId)
            if ("password" not in request.form):
                return Response("Please provide a new password.", status=400)
            
            newPassword = request.form["password"]
            confirmPassword = request.form["confirmPassword"]

            if (newPassword != confirmPassword): 
                return Response("Password and Confirm Password fields must be the same", status=403)
            
            if (AuthenticationService.resetPasswordSame(user, newPassword)): 
                return Response("Please choose a password that you haven't used before", status=403)
            
            AuthenticationService.setUserResetID(user, "")
            AuthenticationService.changePassword(user.email, newPassword)
            return Response("Password sucessfully updated", status=200)
        except:
                return Response("Your password reset link is either invalid or expired. Please request a new one.", status=403)

@auth_ns.route("/verifySession")
class VerifySession(Resource):
    @auth_ns.doc(
        responses={
            200: "Password sucessfully updated",
            400: "Invalid session. Please login again.",
            401: "Your session has expired. Please login again.",
            401: "Your session was not found. Please login again."

        },
        params={
            'sessionId': {'in': 'formData', 'required': True},
        }
    )  
    def post(self):  
        try:
            sessionId = request.form["sessionId"]
            user = AuthenticationService.verifySessionAndReturnUser(sessionId)
            if not user:
                return Response("Your session has expired. Please login again.",status=401)
            else:
                return Response(user.email, status=200)
        except DoesNotExist as e:
            return Response("Your session was not found. Please login again.",status=401)
        except ValueError as e:
            return Response("Invalid session. Please login again.", status=400)  

@auth_ns.route("/delete-account")
class DeleteAccount(Resource):
    @auth_ns.doc(
        responses={
            200: "Account deleted.",
            403: "Error getting user from session.",
            403: "Error deleting user.",
            403: "Error deleting datasets."
        },
        params={
            'sessionId': {'in': 'formData', 'required': True},
        }
    )   
    def post(self):  
        try:
            form = request.form #the form submitted
            SID = form["sessionId"] #gets SID from cookie
            session = AuthenticationService.getSession(SID) #uses SID to get session from db
            user = session["user"] #gets user from session

            # found user, remove their datasets
            try:
                Dataset.objects(author=user).delete()
            except:
                return Response("Error deleting datasets.",status=403)
            # once datasets have been removed, remove user from users
            try:
                # log out before deletion
                sessionId = request.form["sessionId"]
                AuthenticationService.logout(sessionId)
                # remove user with query by email
                user.delete()
            except:
                return Response("Error deleting user.", status=403)
            return Response("Account deleted.", status=200)
        except:
            return Response("Error getting user from session.", status=403) 
    
