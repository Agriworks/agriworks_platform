from flask import Flask
from mongoengine import connect


db = connect('agriworks')

def create_app():
    app = Flask(__name__)

    with app.app_context():
        import Endpoints.AdminEndpoints as admin
        import Endpoints.AuthenticationEndpoints as auth
        
        app.register_blueprint(admin.admin)
        app.register_blueprint(auth.auth)
        return app

