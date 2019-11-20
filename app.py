from flask import Flask
from mongoengine import connect
from flask_cors import CORS

db = connect('agriworks')

def create_app():
    app = Flask(__name__)

    #CORS for the backend server and frontend to communicate with each other
    app.config['SECRET_KEY'] = 'secret'
    app.config['CORS_HEADERS'] = 'Content-Type'
    CORS(app, resources={r"*": {"origins": "http://localhost:8080"}})

    with app.app_context():
        import Controllers.AdminController as admin
        import Controllers.AuthenticationController as auth
        
        app.register_blueprint(admin.admin)
        app.register_blueprint(auth.auth)
        return app

