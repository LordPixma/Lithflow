# app/blueprints/prices/routes.py
from flask import render_template, jsonify, request
from flask_login import login_required, current_user
from app import db
from app.blueprints.prices import prices_bp
from app.models.price import LithiumPrice, RelatedCommodityPrice, PriceForecast
from app.utils.access_control import premium_required
from sqlalchemy import func
import datetime

@prices_bp.route('/dashboard')
@login_required
def dashboard():
    """Main price dashboard view"""
    # Get compounds and regions for filtering
    compounds = db.session.query(LithiumPrice.compound).distinct().all()
    regions = db.session.query(LithiumPrice.region).distinct().all()
    
    return render_template(
        'prices/dashboard.html',
        compounds=[c[0] for c in compounds],
        regions=[r[0] for r in regions]
    )

@prices_bp.route('/api/price-data')
@login_required
def price_data():
    """API endpoint to get price data for charts"""
    compound = request.args.get('compound', 'lithium carbonate')
    region = request.args.get('region', 'China')
    period = request.args.get('period', '1y')  # 1m, 3m, 6m, 1y, all
    
    # Calculate date range based on period
    end_date = datetime.date.today()
    if period == '1m':
        start_date = end_date - datetime.timedelta(days=30)
    elif period == '3m':
        start_date = end_date - datetime.timedelta(days=90)
    elif period == '6m':
        start_date = end_date - datetime.timedelta(days=180)
    elif period == '1y':
        start_date = end_date - datetime.timedelta(days=365)
    else:  # all
        start_date = datetime.date(2000, 1, 1)  # arbitrary past date
    
    # Query price data
    prices = LithiumPrice.query.filter(
        LithiumPrice.compound == compound,
        LithiumPrice.region == region,
        LithiumPrice.date >= start_date,
        LithiumPrice.date <= end_date
    ).order_by(LithiumPrice.date).all()
    
    # Format data for chart
    price_data = [{
        'date': price.date.strftime('%Y-%m-%d'),
        'price': price.price,
        'low': price.price_low,
        'high': price.price_high
    } for price in prices]
    
    return jsonify(price_data)

@prices_bp.route('/regional-comparison')
@login_required
def regional_comparison():
    """View for comparing prices across regions"""
    compounds = db.session.query(LithiumPrice.compound).distinct().all()
    regions = db.session.query(LithiumPrice.region).distinct().all()
    
    return render_template(
        'prices/regional_comparison.html',
        compounds=[c[0] for c in compounds],
        regions=[r[0] for r in regions]
    )

@prices_bp.route('/correlation')
@login_required
@premium_required
def correlation():
    """View for price correlation with related commodities (premium)"""
    compounds = db.session.query(LithiumPrice.compound).distinct().all()
    commodities = db.session.query(RelatedCommodityPrice.commodity).distinct().all()
    
    return render_template(
        'prices/correlation.html',
        compounds=[c[0] for c in compounds],
        commodities=[c[0] for c in commodities]
    )

@prices_bp.route('/forecast')
@login_required
@premium_required
def forecast():
    """View for price forecasting (premium)"""
    compounds = db.session.query(LithiumPrice.compound).distinct().all()
    regions = db.session.query(LithiumPrice.region).distinct().all()
    
    return render_template(
        'prices/forecast.html',
        compounds=[c[0] for c in compounds],
        regions=[r[0] for r in regions]
    )

@prices_bp.route('/api/forecast-data')
@login_required
@premium_required
def forecast_data():
    """API endpoint to get forecast data"""
    compound = request.args.get('compound', 'lithium carbonate')
    region = request.args.get('region', 'China')
    
    # Get latest forecast
    latest_date = db.session.query(func.max(PriceForecast.created_date)).scalar()
    
    # Query forecast data
    forecasts = PriceForecast.query.filter(
        PriceForecast.compound == compound,
        PriceForecast.region == region,
        PriceForecast.created_date == latest_date
    ).order_by(PriceForecast.forecast_date).all()
    
    # Format data for chart
    forecast_data = [{
        'date': forecast.forecast_date.strftime('%Y-%m-%d'),
        'price': forecast.forecast_price,
        'low': forecast.forecast_low,
        'high': forecast.forecast_high,
        'confidence': forecast.confidence
    } for forecast in forecasts]
    
    return jsonify(forecast_data)