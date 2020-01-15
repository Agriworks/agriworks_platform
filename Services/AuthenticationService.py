from flask import Blueprint
from flask import current_app as app 
from flask import request, redirect, url_for
from functools import wraps
from app import db
from uuid import uuid4
from Models.User import User
from Models.Session import Session 
from mongoengine import ValidationError

import hashlib

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
    """
    def authenticate(self,email,password):
        hashed = self.saltPassword(password)
        user = self.getUser(email)
        if not user:
            return False
        if hashed != user.password:
            return False
        """
        sessionId = create session 
        create cookie 
        return cookie object here 
        """

        sessionId = Session(user=user)
        Session.objects(user=user).update(upsert=True, sessionId=sessionId.sessionId, date_created=sessionId.date_created)
        return sessionId
    
    """
    Save the user to the database upon signup if they don't exist
    """
    def save(self, user): 
        if self.getUser(user.email): 
            return False
        else:
            user.password = self.saltPassword(user.password)
            user.save()
            return True
          
    """
     Takes a password and returns a hashed version of it
    """
    def saltPassword(self, password):

        yummyYummySalty = "dHw33Th"
        db_password = password+yummyYummySalty
        hasher = hashlib.sha256(db_password.encode())
        hashLevelOne = hasher.hexdigest()
        supaHasher = hashlib.sha256(hashLevelOne.encode())
        hashLevelTwo = supaHasher.hexdigest()
        
        return hashLevelTwo
     
    """
    New user signup
    """
    def signup(self, document):
        user = User(
            firstName=document["firstName"], lastName=document["lastName"], email=document["email"], isAdmin = False,
            password=document["password"])
        error = None
        try:
            user.validate()  # check if its an error with the type entered
            if (self.save(user)):
                success = True
            else:
                success = False
                error = "DuplicateError"
        except ValidationError:  # If error occurs, it means its an error in the typing
            error = "TypeError"
            success = False
        
        return success, error

    def changeEmail(self, oldEmail, newEmail):
        User.objects.get(email=oldEmail).update(email=newEmail)

    def changePassword(self, email, password):
        User.objects.get(email=email).update(password=self.saltPassword(password))   

    def getSession(self, sessionID):
        return Session.objects.get(sessionId=sessionID)

    def logout(self, sessionID):
        session = self.getSession(sessionID)
        session.delete()
        return True
            
