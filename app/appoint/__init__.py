from flask import Blueprint

appoint = Blueprint('appoint', __name__, template_folder="templates", static_folder="static")

from . import appoint_routes