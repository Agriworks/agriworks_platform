from flask import Flask

def create_app():
    """Construct core application"""
    app = Flask(__name__)

    #Initialize plugins here 

    #Register all the components of the application here
    with app.app_context():
        import auth.routes as auth
        import data.routes as data
        
        app.register_blueprint(auth.auth_bp)
        app.register_blueprint(data.data_bp)

        return app