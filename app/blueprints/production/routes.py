# app/blueprints/production/routes.py
from flask import render_template, jsonify, request
from flask_login import login_required, current_user
from app.blueprints.production import production_bp
from app.models.production import (
    LithiumMine, MineProduction, ProcessingPlant, 
    ProcessingProduction, ProjectDevelopment
)
from app.utils.access_control import premium_required
from app import db
from sqlalchemy import func
import datetime

@production_bp.route('/mine-dashboard')
@login_required
def mine_dashboard():
    """View for mine production dashboard"""
    countries = db.session.query(LithiumMine.country).distinct().all()
    mine_types = db.session.query(LithiumMine.type).distinct().all()
    
    return render_template(
        'production/mine_dashboard.html',
        countries=[c[0] for c in countries],
        mine_types=[t[0] for t in mine_types],
        current_year=datetime.datetime.now().year
    )

@production_bp.route('/api/mine-data')
@login_required
def mine_data():
    """API endpoint for mine production data"""
    country = request.args.get('country', None)
    mine_type = request.args.get('type', None)
    year = request.args.get('year', datetime.datetime.now().year)
    
    # Build filter conditions
    filters = []
    if country:
        filters.append(LithiumMine.country == country)
    if mine_type:
        filters.append(LithiumMine.type == mine_type)
    
    # Query mines with filters
    mines = LithiumMine.query.filter(*filters).all()
    mine_ids = [mine.id for mine in mines]
    
    # Query production data for these mines in the specified year
    production_data = MineProduction.query.filter(
        MineProduction.mine_id.in_(mine_ids),
        MineProduction.year == int(year)
    ).all()
    
    # Format data for visualization
    result = []
    for mine in mines:
        mine_production = [p for p in production_data if p.mine_id == mine.id]
        annual_data = next((p for p in mine_production if p.quarter is None), None)
        quarterly_data = [p for p in mine_production if p.quarter is not None]
        
        mine_data = {
            'id': mine.id,
            'name': mine.name,
            'company': mine.company,
            'country': mine.country,
            'type': mine.type,
            'status': mine.status,
            'capacity': mine.capacity,
            'annual_production': annual_data.production if annual_data else None,
            'quarterly_production': [
                {
                    'quarter': p.quarter,
                    'production': p.production,
                    'is_estimate': p.is_estimate
                } for p in sorted(quarterly_data, key=lambda x: x.quarter)
            ] if quarterly_data else []
        }
        result.append(mine_data)
    
    return jsonify(result)

@production_bp.route('/processing-dashboard')
@login_required
def processing_dashboard():
    """View for processing plant dashboard"""
    countries = db.session.query(ProcessingPlant.country).distinct().all()
    products = db.session.query(ProcessingPlant.product).distinct().all()
    
    return render_template(
        'production/processing_dashboard.html',
        countries=[c[0] for c in countries],
        products=[p[0] for p in products],
        current_year=datetime.datetime.now().year
    )

@production_bp.route('/project-pipeline')
@login_required
@premium_required
def project_pipeline():
    """View for lithium project pipeline tracking (premium)"""
    countries = db.session.query(ProjectDevelopment.country).distinct().all()
    project_types = db.session.query(ProjectDevelopment.project_type).distinct().all()
    statuses = db.session.query(ProjectDevelopment.status).distinct().all()
    
    return render_template(
        'production/project_pipeline.html',
        countries=[c[0] for c in countries],
        project_types=[t[0] for t in project_types],
        statuses=[s[0] for s in statuses]
    )

@production_bp.route('/api/project-timeline')
@login_required
@premium_required
def project_timeline():
    """API endpoint for project development timeline data"""
    project_name = request.args.get('project', None)
    country = request.args.get('country', None)
    
    # Build filter conditions
    filters = []
    if project_name:
        filters.append(ProjectDevelopment.project_name == project_name)
    if country:
        filters.append(ProjectDevelopment.country == country)
    
    # Query project development data
    projects = (
        db.session.query(
            ProjectDevelopment.project_name,
            ProjectDevelopment.company,
            ProjectDevelopment.country,
            ProjectDevelopment.project_type
        )
        .filter(*filters)
        .distinct()
        .all()
    )
    
    result = []
    for project in projects:
        project_name, company, country, project_type = project
        
        # Get all milestones for this project
        milestones = (
            ProjectDevelopment.query
            .filter(ProjectDevelopment.project_name == project_name)
            .order_by(ProjectDevelopment.date)
            .all()
        )
        
        project_data = {
            'name': project_name,
            'company': company,
            'country': country,
            'type': project_type,
            'milestones': [
                {
                    'date': milestone.date.strftime('%Y-%m-%d'),
                    'status': milestone.status,
                    'description': milestone.milestone,
                    'investment': milestone.investment,
                    'expected_completion': (
                        milestone.expected_completion.strftime('%Y-%m-%d')
                        if milestone.expected_completion else None
                    )
                } for milestone in milestones
            ]
        }
        result.append(project_data)
    
    return jsonify(result)

@production_bp.route('/country-overview')
@login_required
def country_overview():
    """View for country-level production overview"""
    return render_template('production/country_overview.html')

@production_bp.route('/api/country-production')
@login_required
def country_production():
    """API endpoint for country-level production data"""
    year = request.args.get('year', datetime.datetime.now().year)
    
    # Get all countries with mines
    countries = db.session.query(LithiumMine.country).distinct().all()
    countries = [c[0] for c in countries]
    
    result = []
    for country in countries:
        # Get mines in this country
        mines = LithiumMine.query.filter(LithiumMine.country == country).all()
        mine_ids = [mine.id for mine in mines]
        
        # Get production data for these mines
        production_query = (
            db.session.query(func.sum(MineProduction.production))
            .filter(
                MineProduction.mine_id.in_(mine_ids),
                MineProduction.year == int(year),
                MineProduction.quarter.is_(None)  # Annual data only
            )
        )
        
        total_production = production_query.scalar() or 0
        
        # Get processing plants in this country
        plants = ProcessingPlant.query.filter(ProcessingPlant.country == country).all()
        plant_ids = [plant.id for plant in plants]
        
        # Get production data for these plants
        processing_query = (
            db.session.query(func.sum(ProcessingProduction.production))
            .filter(
                ProcessingProduction.plant_id.in_(plant_ids),
                ProcessingProduction.year == int(year),
                ProcessingProduction.quarter.is_(None)  # Annual data only
            )
        )
        
        total_processing = processing_query.scalar() or 0
        
        country_data = {
            'country': country,
            'mine_count': len(mines),
            'mine_production': total_production,
            'plant_count': len(plants),
            'processing_production': total_processing
        }
        result.append(country_data)
    
    return jsonify(result)