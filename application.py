import yaml
from flask import Flask
from mongoengine import connect
from flask_cors import CORS

# read in remote db username and password
creds = yaml.safe_load(open("creds.yaml", "r"))
dbHostUri = "mongodb+srv://" + creds["db_user"] + ":" + creds["db_password"] + \
    "@cluster0-ollas.mongodb.net/test?retryWrites=true&w=majority&ssl=true&ssl_cert_reqs=CERT_NONE"

db = connect(host=dbHostUri)

application = Flask(__name__)

@application.route("/")
def index():
    return "Agriworks is online"

application.config.update(dict(
    MAIL_SERVER='smtp.gmail.com',
    MAIL_PORT=587,
    MAIL_USE_TLS=True,
    MAIL_USE_SSL=False,
    MAIL_USERNAME=creds["MAIL_USER"],
    MAIL_PASSWORD=creds["MAIL_PASS"],
    MAIL_DEFAULT_SENDER="noreply.agriworks@gmail.com"
))

def importControllers():
    with application.app_context():
        import Controllers.AdminController as admin
        import Controllers.AuthenticationController as auth
        import Controllers.UploadController as upload
        import Controllers.DatasetController as dataset

        application.register_blueprint(admin.admin)
        application.register_blueprint(auth.auth)
        application.register_blueprint(upload.upload)
        application.register_blueprint(dataset.dataset)

importControllers()

if __name__ == "__main__":
    application.run()