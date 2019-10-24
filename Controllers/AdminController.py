from flask import Blueprint
from flask import current_app as app
from Services.AuthenticationService import AuthenticationService

Authentication = AuthenticationService()

admin = Blueprint("AdminController", __name__, url_prefix="/admin")

@admin.route("/", methods=["GET"])
def index():
    return {"status": "Congradulations, Agriworks is now running on your machine."}

@admin.route("/account", methods=["GET"])
@Authentication.login_required
def account():
    return "This is secure content"