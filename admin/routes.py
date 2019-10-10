from flask import Blueprint
from flask import current_app as app

admin_bp = Blueprint("admin_bp", __name__, template_folder=None, static_folder=None, url_prefix="/admin")

@admin_bp.route("/", methods=["GET"])
def index():
    return "<h1> Congratulations, Agriworks is running </h1>"
