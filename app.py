import yaml
from flask import Flask
from mongoengine import connect
from flask_cors import CORS
import os

# read in remote db username and password
dbCreds = yaml.safe_load(open("creds.yaml", "r"))
dbHostUri = "mongodb+srv://" + dbCreds["db_user"] + ":" + dbCreds["db_password"] + \
    "@cluster0-ollas.mongodb.net/test?retryWrites=true&w=majority&ssl=true&ssl_cert_reqs=CERT_NONE"

db = connect(host=dbHostUri)


def create_app():
    app = Flask(__name__)

    # CORS for the backend server and frontend to communicate with each other
    app.config['SECRET_KEY'] = 'secret'
    app.config['CORS_HEADERS'] = 'Content-Type'
    CORS(app, resources={r"*": {"origins": "*"}})
    # mail
    app.config.update(dict(
        MAIL_SERVER='smtp.gmail.com',
        MAIL_PORT=587,
        MAIL_USE_TLS=True,
        MAIL_USE_SSL=False,
        MAIL_USERNAME=os.environ.get("MAIL_USER"),
        MAIL_PASSWORD=os.environ.get("MAIL_PASS"),
        MAIL_DEFAULT_SENDER="noreply.agriworks@gmail.com"
    ))
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
