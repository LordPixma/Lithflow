from flask import Blueprint

prices_bp = Blueprint('prices', __name__, url_prefix='/prices')

from . import routes
