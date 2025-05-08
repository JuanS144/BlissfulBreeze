from flask import Blueprint

report_bp = Blueprint('report_bp',__name__, template_folder='templates', static_folder='static')

from . import routes