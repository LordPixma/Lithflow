from flask import Blueprint

market_analytics_bp = Blueprint('market_analytics', __name__, url_prefix='/market_analytics')

from . import routes
