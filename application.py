from flask import Flask, send_file, send_from_directory
from mongoengine import connect
import yaml
import boto3
from Response import Response
from Services.EndpointProtectionService import authRequired, NON_PROTECTED_ENDPOINTS
import os

STATIC_DIRECTORIES = ["js", "css", "img", "fonts"]
STATIC_DIRECTORY_ROOT = "./dist/"
STATIC_ASSETS_DIRECTORY_ROOT = "./dist/assets/"

# Instantiate application 
application = Flask(__name__)
application.env = application.config["ENV"]

# Instantiate connection to database
if (application.env == "production"):
    creds = {}
    creds["DB_USER"] = os.getenv("DB_USER")
    creds["DB_PASSWORD"] = os.getenv("DB_PASSWORD")
    creds["AWS_ACCESS_KEY"] = os.getenv("AWS_ACCESS_KEY")
    creds["AWS_SECRET_KEY"] = os.getenv("AWS_SECRET_KEY")
    creds["MAIL_USER"] = os.getenv("MAIL_USER")
    creds["SENDGRID_API_KEY"] = os.getenv("SENDGRID_API_KEY")
else:
    creds = yaml.safe_load(open("creds.yaml", "r"))

dbHostUri = "mongodb+srv://" + creds["DB_USER"] + ":" + creds["DB_PASSWORD"] + \
    "@cluster0-ollas.mongodb.net/test?retryWrites=true&w=majority&ssl=true&ssl_cert_reqs=CERT_NONE"
db = connect(host=dbHostUri)

# Instantiate connection to AWS
awsSession = boto3.Session(
    aws_access_key_id=creds["AWS_ACCESS_KEY"],
    aws_secret_access_key=creds["AWS_SECRET_KEY"]
)


if (application.env == "production"):
    # Route handlers for FE
    @application.route("/assets/<string:requestedStaticDirectory>/<path:path>")
    def sendStaticComponent(requestedStaticDirectory, path):
        if requestedStaticDirectory not in STATIC_DIRECTORIES:
            return Response("Not a valid static asset directory", status=400)
        return send_from_directory(STATIC_ASSETS_DIRECTORY_ROOT + requestedStaticDirectory, path)

    @application.route("/")
    def index():
        return send_file(STATIC_DIRECTORY_ROOT + "index.html")

    @application.errorhandler(404)
    def rerouteToIndex(e):
        return send_file(STATIC_DIRECTORY_ROOT + "index.html")

# Link aws session to application object
application.awsSession = awsSession

# Setup mail 
application.config.update(dict(
    MAIL_USERNAME=creds["MAIL_USER"],
    SENDGRID_KEY=creds["SENDGRID_API_KEY"]
))

#Define root url of site 
if (application.env == "production"):
    application.rootUrl = "https://agri-works.org"
else:
    application.rootUrl = "http://localhost:8080"

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

#Default error handler
@application.errorhandler(500)
def handleServerError(e):
    return Response("Internal server error", status=500)

#Protect all endpoints by wrapping relevant view function with authentication required function.
viewFunctions = application.view_functions
for key in viewFunctions.keys():
    if (key not in NON_PROTECTED_ENDPOINTS):    
        viewFunctions[key] = authRequired(viewFunctions[key])

if __name__ == "__main__":
    application.run(port=4000, debug=True)