from flask import Blueprint
from flask import current_app as app
from Controllers.IndexController import IndexController
from Services.AuthenticationService import Authentication


Authentication = Authentication()
IndexController = IndexController()

admin = Blueprint("AdminEndpoints", __name__, url_prefix="/admin")

@admin.route("/index", methods=["GET"])
def index():
    return IndexController.get()

@admin.route("/account", methods=["GET"])
@Authentication.login_required
def account():
    return "This is secure content"