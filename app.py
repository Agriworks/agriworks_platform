import yaml
from flask import Flask
from mongoengine import connect
from flask_cors import CORS

dbCreds = yaml.safe_load(open("creds.yaml", "r")) #read in remote db username and password
dbHostUri = "mongodb+srv://" + dbCreds["db_user"] + ":" + dbCreds["db_password"] + "@cluster0-ollas.mongodb.net/test?retryWrites=true&w=majority&ssl=true&ssl_cert_reqs=CERT_NONE"

db = connect(host=dbHostUri)


def create_app():
    app = Flask(__name__)

    #CORS for the backend server and frontend to communicate with each other
    app.config['SECRET_KEY'] = 'secret'
    app.config['CORS_HEADERS'] = 'Content-Type'
    CORS(app, resources={r"*": {"origins": "*"}})

    with app.app_context():
        import Controllers.AdminController as admin
        import Controllers.AuthenticationController as auth
        import Controllers.UploadController as upload
        import Controllers.DatasetController as dataset
        
        app.register_blueprint(admin.admin)
        app.register_blueprint(auth.auth)
        app.register_blueprint(upload.upload)
        app.register_blueprint(dataset.dataset)
        return app

