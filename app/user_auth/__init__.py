from flask import Blueprint

user_auth = Blueprint('user_auth',__name__, template_folder='templates', static_folder='static')

from . import user_routes