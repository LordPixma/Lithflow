# app/models/production.py
from app import db
import datetime

class LithiumMine(db.Model):
    """Model for lithium mining operations"""
    __tablename__ = 'lithium_mines'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    company = db.Column(db.String(100), nullable=False)
    country = db.Column(db.String(50), nullable=False)
    region = db.Column(db.String(50))  # geographical region
    type = db.Column(db.String(50))  # brine, hard rock, etc.
    status = db.Column(db.String(50))  # operational, development, exploration
    capacity = db.Column(db.Float)  # annual production capacity in tons
    start_year = db.Column(db.Integer)  # year production started/expected
    coordinates = db.Column(db.String(50))  # latitude,longitude format
    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    
    # Relationships
    production_data = db.relationship('MineProduction', backref='mine', lazy=True)
    
    def __repr__(self):
        return f'<LithiumMine {self.name}>'

class MineProduction(db.Model):
    """Model for lithium mine production data"""
    __tablename__ = 'mine_production'
    
    id = db.Column(db.Integer, primary_key=True)
    mine_id = db.Column(db.Integer, db.ForeignKey('lithium_mines.id'), nullable=False)
    year = db.Column(db.Integer, nullable=False)
    quarter = db.Column(db.Integer)  # 1-4, NULL for annual data
    production = db.Column(db.Float)  # in LCE (Lithium Carbonate Equivalent) tons
    grade = db.Column(db.Float)  # lithium content/grade
    cost = db.Column(db.Float)  # production cost per ton
    source = db.Column(db.String(100))  # data source
    is_estimate = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    
    __table_args__ = (
        db.UniqueConstraint('mine_id', 'year', 'quarter', name='unique_mine_period'),
    )
    
    def __repr__(self):
        period = f'Q{self.quarter}' if self.quarter else 'Annual'
        return f'<MineProduction {self.mine.name} {self.year} {period}>'

class ProcessingPlant(db.Model):
    """Model for lithium processing facilities"""
    __tablename__ = 'processing_plants'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    company = db.Column(db.String(100), nullable=False)
    country = db.Column(db.String(50), nullable=False)
    type = db.Column(db.String(50))  # conversion, refining, etc.
    status = db.Column(db.String(50))  # operational, construction, planned
    capacity = db.Column(db.Float)  # annual processing capacity in tons
    product = db.Column(db.String(50))  # carbonate, hydroxide, etc.
    start_year = db.Column(db.Integer)  # year operation started/expected
    coordinates = db.Column(db.String(50))  # latitude,longitude format
    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    
    # Relationships
    production_data = db.relationship('ProcessingProduction', backref='plant', lazy=True)
    
    def __repr__(self):
        return f'<ProcessingPlant {self.name}>'

class ProcessingProduction(db.Model):
    """Model for lithium processing plant production data"""
    __tablename__ = 'processing_production'
    
    id = db.Column(db.Integer, primary_key=True)
    plant_id = db.Column(db.Integer, db.ForeignKey('processing_plants.id'), nullable=False)
    year = db.Column(db.Integer, nullable=False)
    quarter = db.Column(db.Integer)  # 1-4, NULL for annual data
    production = db.Column(db.Float)  # in tons
    capacity_utilization = db.Column(db.Float)  # percentage of capacity utilized
    source = db.Column(db.String(100))  # data source
    is_estimate = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    
    __table_args__ = (
        db.UniqueConstraint('plant_id', 'year', 'quarter', name='unique_plant_period'),
    )
    
    def __repr__(self):
        period = f'Q{self.quarter}' if self.quarter else 'Annual'
        return f'<ProcessingProduction {self.plant.name} {self.year} {period}>'

class ProjectDevelopment(db.Model):
    """Model for tracking lithium project development"""
    __tablename__ = 'project_developments'
    
    id = db.Column(db.Integer, primary_key=True)
    project_name = db.Column(db.String(100), nullable=False)
    company = db.Column(db.String(100), nullable=False)
    country = db.Column(db.String(50), nullable=False)
    project_type = db.Column(db.String(50), nullable=False)  # mine, processing, etc.
    date = db.Column(db.Date, nullable=False)
    status = db.Column(db.String(50), nullable=False)  # study, permit, construction, etc.
    milestone = db.Column(db.String(255))  # specific milestone reached
    investment = db.Column(db.Float)  # investment amount in USD
    capacity = db.Column(db.Float)  # planned capacity
    expected_completion = db.Column(db.Date)
    source = db.Column(db.String(100))
    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    
    def __repr__(self):
        return f'<ProjectDevelopment {self.project_name} {self.date}>'
