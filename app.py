from flask import Flask
from mongoengine import connect
import pandas as pd;
from pandas import DataFrame, read_csv;


db = connect('agriworks')

def create_app():
    app = Flask(__name__)

    with app.app_context():
        import Controllers.AdminController as admin
        import Controllers.AuthenticationController as auth
        
        app.register_blueprint(admin.admin)
        app.register_blueprint(auth.auth)
        return app

