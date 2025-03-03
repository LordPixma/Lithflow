# app/models/market.py
from app import db
import datetime

class SupplyDemand(db.Model):
    """Model for lithium supply-demand balance data"""
    __tablename__ = 'supply_demand_balance'
    
    id = db.Column(db.Integer, primary_key=True)
    year = db.Column(db.Integer, nullable=False)
    quarter = db.Column(db.Integer)  # 1-4, NULL for annual data
    supply = db.Column(db.Float, nullable=False)  # in tons of LCE
    demand = db.Column(db.Float, nullable=False)  # in tons of LCE
    balance = db.Column(db.Float, nullable=False)  # surplus/deficit
    is_forecast = db.Column(db.Boolean, default=False)
    source = db.Column(db.String(100))
    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    
    def __repr__(self):
        period = f'Q{self.quarter}' if self.quarter else 'Annual'
        forecast = 'Forecast' if self.is_forecast else 'Actual'
        return f'<SupplyDemand {self.year} {period} {forecast}>'

class EVMarketData(db.Model):
    """Model for electric vehicle market data"""
    __tablename__ = 'ev_market_data'
    
    id = db.Column(db.Integer, primary_key=True)
    year = db.Column(db.Integer, nullable=False)
    quarter = db.Column(db.Integer)  # 1-4, NULL for annual data
    region = db.Column(db.String(50), nullable=False)
    ev_sales = db.Column(db.Integer, nullable=False)  # units sold
    ev_penetration = db.Column(db.Float)  # % of total vehicle sales
    lithium_demand = db.Column(db.Float)  # in tons of LCE
    avg_battery_size = db.Column(db.Float)  # in kWh
    is_forecast = db.Column(db.Boolean, default=False)
    source = db.Column(db.String(100))
    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    
    def __repr__(self):
        period = f'Q{self.quarter}' if self.quarter else 'Annual'
        return f'<EVMarketData {self.region} {self.year} {period}>'

class BatteryChemistry(db.Model):
    """Model for battery chemistry trend data"""
    __tablename__ = 'battery_chemistry'
    
    id = db.Column(db.Integer, primary_key=True)
    year = db.Column(db.Integer, nullable=False)
    quarter = db.Column(db.Integer)  # 1-4, NULL for annual data
    chemistry_type = db.Column(db.String(50), nullable=False)  # NMC, LFP, etc.
    market_share = db.Column(db.Float, nullable=False)  # % of total market
    lithium_intensity = db.Column(db.Float)  # kg of lithium per kWh
    region = db.Column(db.String(50))  # regional breakdown
    is_forecast = db.Column(db.Boolean, default=False)
    source = db.Column(db.String(100))
    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    
    def __repr__(self):
        period = f'Q{self.quarter}' if self.quarter else 'Annual'
        return f'<BatteryChemistry {self.chemistry_type} {self.year} {period}>'

class RegulationEvent(db.Model):
    """Model for regulatory events affecting lithium market"""
    __tablename__ = 'regulation_events'
    
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, nullable=False)
    country = db.Column(db.String(50), nullable=False)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    category = db.Column(db.String(50))  # environmental, mining, trade, etc.
    impact_level = db.Column(db.String(20))  # high, medium, low
    market_impact = db.Column(db.Text)  # description of potential market impact
    source = db.Column(db.String(100))
    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    
    def __repr__(self):
        return f'<RegulationEvent {self.country} {self.date}>'

class TradeFlow(db.Model):
    """Model for lithium trade flow data"""
    __tablename__ = 'trade_flows'
    
    id = db.Column(db.Integer, primary_key=True)
    year = db.Column(db.Integer, nullable=False)
    quarter = db.Column(db.Integer)  # 1-4, NULL for annual data
    exporter = db.Column(db.String(50), nullable=False)  # country/region
    importer = db.Column(db.String(50), nullable=False)  # country/region
    material_type = db.Column(db.String(50), nullable=False)  # raw ore, carbonate, hydroxide, etc.
    volume = db.Column(db.Float, nullable=False)  # in tons
    value = db.Column(db.Float)  # in USD
    source = db.Column(db.String(100))
    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    
    def __repr__(self):
        period = f'Q{self.quarter}' if self.quarter else 'Annual'
        return f'<TradeFlow {self.exporter} to {self.importer} {self.year} {period}>'