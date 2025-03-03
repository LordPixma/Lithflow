# app/__init__.py
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_wtf.csrf import CSRFProtect



from app.config import config

# Initialize extensions
db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()
csrf = CSRFProtect()

def create_app(config_name='default'):
    """Create and configure the Flask application"""
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    
    # Initialize extensions with app
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    csrf.init_app(app)
    
    from app.models.user import AnonymousUser
    
    # Set up login configuration
    login_manager.anonymous_user = AnonymousUser
    login_manager.login_view = 'auth.login'
    login_manager.login_message_category = 'info'
    
    # Register blueprints
    from app.blueprints.auth import auth_bp
    from app.blueprints.prices import prices_bp
    from app.blueprints.production import production_bp
    from app.blueprints.market_analytics import market_bp
    from app.blueprints.news import news_bp
    from app.blueprints.user import user_bp
    from app.blueprints.main import main_bp
    
    app.register_blueprint(auth_bp)
    app.register_blueprint(prices_bp)
    app.register_blueprint(production_bp)
    app.register_blueprint(market_bp)
    app.register_blueprint(news_bp)
    app.register_blueprint(user_bp)
    app.register_blueprint(main_bp)
    
    # Register error handlers
    from app.utils.error_handlers import register_error_handlers
    register_error_handlers(app)
    
    return app