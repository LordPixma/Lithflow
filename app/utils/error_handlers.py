# app/utils/error_handlers.py
from flask import render_template

def register_error_handlers(app):
    """Register error handlers for the application"""
    
    @app.errorhandler(404)
    def page_not_found(e):
        return render_template('errors/404.html'), 404
    
    @app.errorhandler(403)
    def forbidden(e):
        return render_template('errors/403.html'), 403
    
    @app.errorhandler(500)
    def internal_server_error(e):
        return render_template('errors/500.html'), 500
    
    @app.errorhandler(401)
    def unauthorized(e):
        return render_template('errors/401.html'), 401