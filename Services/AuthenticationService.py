from flask import Blueprint
from flask import current_app as app 
from flask import request, redirect, url_for
from functools import wraps
from app import db
from uuid import uuid4
from Models.User import User
from Models.Session import Session 
from datetime import datetime

import hashlib
import uuid

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
    def getUser(self, **kwargs):
        if not User.objects(**kwargs):
            return False

        user = User.objects.get(**kwargs) #use objects.get to retreive one result
        
        return user

    """
    Authenticate the user (Login). 
    @param: email 
    @param: password
    @return: unique session id
    """
    def authenticate(self,email,password):
        hashedPassword = self.saltPassword(password)
        user = self.getUser(email=email)

        if not user:
            return False

        if hashedPassword != user.password:
            return False

        session = Session(user=user)
        session.save()
        return session
    
    """
    Save the user to the database upon signup if they don't exist
    """
    def save(self, user): 
        if self.getUser(email=user.email): 
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
    Currently, all users will not be administrators.
    """
    def signup(self, document):
        user = User(
            firstName=document["firstName"], 
            lastName=document["lastName"], 
            email=document["email"],
            password=document["password"],
            isAdmin=False
            )
    
        user.validate()  # TODO: enclose this in a try/catch block /check if its an error with the type entered

        if (self.save(user)):
            return True
        else:
            return False

    def emailIsAlreadyInUse(self, email):
        return User.objects(email=email)
        
    def changeEmail(self, oldEmail, newEmail):
        User.objects.get(email=oldEmail).update(email=newEmail)

    def changePassword(self, email, password):
        User.objects.get(email=email).update(password=self.saltPassword(password))   

    def getSession(self, sessionId):
        sessionUUID = uuid.UUID(sessionId)
        return Session.objects.get(sessionId=sessionUUID)

    def logout(self, sessionId):
        session = self.getSession(sessionId)
        if (session):
            session.delete()
        else:
            raise
            
    
    def verifySessionAndReturnUser(self, sessionId):
        session = self.getSession(sessionId)
        if (datetime.utcnow() < session.dateExpires):
            return User.objects.get(id=session.user.id)
        else:
            return False