from flask import Blueprint
from flask import current_app as app

data_bp = Blueprint("data_bp", __name__, template_folder=None, static_folder=None, url_prefix="/data")

@data_bp.route("/index", methods=["GET"])
def index():
    return "Index of Data"
