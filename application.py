from flask import Flask, make_response, send_file
from flask_socketio import SocketIO
#from Controllers.StreamingDatasetController import stream
from mongoengine import connect
import yaml
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

# Instantiate socket server
io = SocketIO(application)

@io.on("connect")
def test_connect():
    print("USER CONNECTED")

@io.on("message")
def handle_message(message):
    print("received message" + message)

# Default route to test if backend is online
@application.route("/")
def index():
    return "Agriworks is online"

# Link aws session to application object
application.awsSession = awsSession

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

if __name__ == "__main__":
    io.run(application, port=4000, debug=True)