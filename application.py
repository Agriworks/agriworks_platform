import yaml
from flask import Flask
from mongoengine import connect
import boto3

# Instantiate connection to database
creds = yaml.safe_load(open("creds.yaml", "r"))
dbHostUri = "mongodb+srv://" + creds["DB_USER"] + ":" + creds["DB_PASSWORD"] + \
    "@cluster0-ollas.mongodb.net/test?retryWrites=true&w=majority&ssl=true&ssl_cert_reqs=CERT_NONE"
db = connect(host=dbHostUri)

# Instantiate connection to AWS
awsSession = boto3.Session(
    aws_access_key_id=creds["AWS_ACCESS_KEY"],
    aws_secret_access_key=creds["AWS_SECRET_KEY"]
)

# Instantiate application 
application = Flask(__name__)

# Default route to test if backend is online
@application.route("/")
def index():
    return "Agriworks is online"

# Setup mail 
application.config.update(dict(
    MAIL_SERVER='smtp.gmail.com',
    MAIL_PORT=587,
    MAIL_USE_TLS=True,
    MAIL_USE_SSL=False,
    MAIL_USERNAME=creds["MAIL_USER"],
    MAIL_PASSWORD=creds["MAIL_PASSWORD"],
    MAIL_DEFAULT_SENDER="noreply.agriworks@gmail.com"
))

# Import application controllers. Cannot import from default context due to mutual imports issue
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
