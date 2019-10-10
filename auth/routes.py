from flask import Blueprint
from flask import current_app as app 

auth_bp = Blueprint("auth_bp", __name__, template_folder=None, static_folder=None, url_prefix="/auth")

@auth_bp.route("/index", methods=["GET"])
def index():
    return "Index of Auth"