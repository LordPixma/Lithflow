from flask import Blueprint

user_bp = Blueprint('user', __name__, url_prefix='/user')

from . import routes
