from flask import Blueprint
from flask import current_app as app 
from flask import request, redirect, url_for
from functools import wraps
from app import db
from Models.User import User
from Models.Session import Session 

class AuthenticationService():
    
    def __init__(self):
        return
    
    #TODO: 
    def login_required(self,f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            authenticated = True
            if(not authenticated):
                return "Please login first"
            else:
                return f(*args, **kwargs) #PASSING TO NEXT 
        return decorated_function

    """ 
    Return the user
    """ 
    def getUser(self,email):
        if not User.objects(email=email):
            return False
        return User.objects.get(email=email) #use objects.get to retreive one result

    """
    Authenticate the user
    #TODO: SHAIVYA Hash the inputted password and compare with the password in the DB
    """
    def authenticate(self,email,password):
        user = self.getUser(email)
        if not user:
            return False
        if password != user.password:
            return False
        """
        sessionId = create session 
        create cookie 
        return cookie object here 
        """
        return True
    
    """
    Save the user to the database upon signup if they don't exist
    """
    def save(self, user): 
        if getUser(user.email): 
            return False
        else:
            user.save()
     

