# app/blueprints/market_analytics/routes.py
from flask import render_template, jsonify, request
from flask_login import login_required, current_user
from app import db
from app.blueprints.market_analytics import market_bp
from app.models.market import (
    SupplyDemand, EVMarketData, BatteryChemistry,
    RegulationEvent, TradeFlow
)
from app.utils.access_control import premium_required
from app import db
from sqlalchemy import func
import datetime

@market_bp.route('/supply-demand')
@login_required
def supply_demand():
    """View for supply-demand balance dashboard"""
    return render_template('market/supply_demand.html')

@market_bp.route('/api/supply-demand-data')
@login_required
def supply_demand_data():
    """API endpoint to get supply-demand data"""
    # Get parameters
    start_year = request.args.get('start_year', datetime.datetime.now().year - 5)
    end_year = request.args.get('end_year', datetime.datetime.now().year + 5)
    
    # Query data
    data = SupplyDemand.query.filter(
        SupplyDemand.year >= int(start_year),
        SupplyDemand.year <= int(end_year),
        SupplyDemand.quarter.is_(None)  # Annual data only
    ).order_by(SupplyDemand.year).all()
    
    # Format for chart
    result = [{
        'year': item.year,
        'supply': item.supply,
        'demand': item.demand,
        'balance': item.balance,
        'is_forecast': item.is_forecast
    } for item in data]
    
    return jsonify(result)

@market_bp.route('/ev-tracking')
@login_required
def ev_tracking():
    """View for EV market tracking"""
    regions = db.session.query(EVMarketData.region).distinct().all()
    regions = [r[0] for r in regions]
    
    return render_template(
        'market/ev_tracking.html',
        regions=regions
    )

@market_bp.route('/api/ev-market-data')
@login_required
def ev_market_data():
    """API endpoint to get EV market data"""
    region = request.args.get('region', 'Global')
    start_year = request.args.get('start_year', datetime.datetime.now().year - 5)
    end_year = request.args.get('end_year', datetime.datetime.now().year + 2)
    
    # Query data
    data = EVMarketData.query.filter(
        EVMarketData.region == region,
        EVMarketData.year >= int(start_year),
        EVMarketData.year <= int(end_year),
        EVMarketData.quarter.is_(None)  # Annual data only
    ).order_by(EVMarketData.year).all()
    
    # Format for chart
    result = [{
        'year': item.year,
        'ev_sales': item.ev_sales,
        'ev_penetration': item.ev_penetration,
        'lithium_demand': item.lithium_demand,
        'avg_battery_size': item.avg_battery_size,
        'is_forecast': item.is_forecast
    } for item in data]
    
    return jsonify(result)

@market_bp.route('/battery-chemistry')
@login_required
@premium_required
def battery_chemistry():
    """View for battery chemistry trends (premium)"""
    chemistries = db.session.query(BatteryChemistry.chemistry_type).distinct().all()
    regions = db.session.query(BatteryChemistry.region).distinct().all()
    
    return render_template(
        'market/battery_chemistry.html',
        chemistries=[c[0] for c in chemistries],
        regions=[r[0] for r in regions if r[0] is not None]
    )

@market_bp.route('/api/battery-chemistry-data')
@login_required
@premium_required
def battery_chemistry_data():
    """API endpoint to get battery chemistry data"""
    region = request.args.get('region', 'Global')
    year = request.args.get('year', datetime.datetime.now().year)
    
    # Query data
    filters = [
        BatteryChemistry.year == int(year),
        BatteryChemistry.quarter.is_(None)  # Annual data only
    ]
    
    if region != 'Global':
        filters.append(BatteryChemistry.region == region)
    
    data = BatteryChemistry.query.filter(*filters).all()
    
    # Format for chart
    result = [{
        'chemistry_type': item.chemistry_type,
        'market_share': item.market_share,
        'lithium_intensity': item.lithium_intensity
    } for item in data]
    
    return jsonify(result)

@market_bp.route('/regulatory-impact')
@login_required
@premium_required
def regulatory_impact():
    """View for regulatory impact assessment (premium)"""
    countries = db.session.query(RegulationEvent.country).distinct().all()
    categories = db.session.query(RegulationEvent.category).distinct().all()
    
    return render_template(
        'market/regulatory_impact.html',
        countries=[c[0] for c in countries],
        categories=[c[0] for c in categories if c[0] is not None]
    )

@market_bp.route('/api/regulation-events')
@login_required
@premium_required
def regulation_events():
    """API endpoint to get regulation event data"""
    country = request.args.get('country', None)
    category = request.args.get('category', None)
    start_date = request.args.get('start_date', 
                                (datetime.datetime.now() - datetime.timedelta(days=365)).strftime('%Y-%m-%d'))
    end_date = request.args.get('end_date', datetime.datetime.now().strftime('%Y-%m-%d'))
    
    # Convert string dates to date objects
    start_date = datetime.datetime.strptime(start_date, '%Y-%m-%d').date()
    end_date = datetime.datetime.strptime(end_date, '%Y-%m-%d').date()
    
    # Build filter
    filters = [
        RegulationEvent.date >= start_date,
        RegulationEvent.date <= end_date
    ]
    
    if country:
        filters.append(RegulationEvent.country == country)
    if category:
        filters.append(RegulationEvent.category == category)
    
    # Query data
    events = RegulationEvent.query.filter(*filters).order_by(RegulationEvent.date.desc()).all()
    
    # Format for response
    result = [{
        'id': event.id,
        'date': event.date.strftime('%Y-%m-%d'),
        'country': event.country,
        'title': event.title,
        'description': event.description,
        'category': event.category,
        'impact_level': event.impact_level,
        'market_impact': event.market_impact
    } for event in events]
    
    return jsonify(result)

@market_bp.route('/trade-flows')
@login_required
@premium_required
def trade_flows():
    """View for trade flow visualization (premium)"""
    exporters = db.session.query(TradeFlow.exporter).distinct().all()
    importers = db.session.query(TradeFlow.importer).distinct().all()
    materials = db.session.query(TradeFlow.material_type).distinct().all()
    
    return render_template(
        'market/trade_flows.html',
        exporters=[e[0] for e in exporters],
        importers=[i[0] for i in importers],
        materials=[m[0] for m in materials]
    )

@market_bp.route('/api/trade-flow-data')
@login_required
@premium_required
def trade_flow_data():
    """API endpoint to get trade flow data"""
    year = request.args.get('year', datetime.datetime.now().year - 1)
    material = request.args.get('material', None)
    
    # Build filter
    filters = [
        TradeFlow.year == int(year),
        TradeFlow.quarter.is_(None)  # Annual data only
    ]
    
    if material:
        filters.append(TradeFlow.material_type == material)
    
    # Query data
    flows = TradeFlow.query.filter(*filters).all()
    
    # Format for visualization (nodes and links format for Sankey diagram)
    countries = set()
    for flow in flows:
        countries.add(flow.exporter)
        countries.add(flow.importer)
    
    # Create nodes list
    nodes = [{"id": country, "name": country} for country in countries]
    
    # Create links list
    links = [{
        "source": flow.exporter,
        "target": flow.importer,
        "value": flow.volume,
        "material": flow.material_type
    } for flow in flows]
    
    result = {
        "nodes": nodes,
        "links": links
    }
    
    return jsonify(result)