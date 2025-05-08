from flask import Blueprint

api = Blueprint('api', __name__, template_folder='templates', static_folder='static')

from app.API import auth, users, appointments, routes