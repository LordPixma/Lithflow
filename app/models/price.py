# app/models/price.py
from app import db
import datetime

class LithiumPrice(db.Model):
    """Model for lithium compound prices"""
    __tablename__ = 'lithium_prices'
    
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, nullable=False)
    compound = db.Column(db.String(50), nullable=False)  # carbonate, hydroxide, etc.
    grade = db.Column(db.String(50))  # battery grade, technical grade, etc.
    region = db.Column(db.String(50), nullable=False)  # China, US, Europe, etc.
    price = db.Column(db.Float, nullable=False)  # in USD/ton
    price_low = db.Column(db.Float)  # for price ranges
    price_high = db.Column(db.Float)  # for price ranges
    currency = db.Column(db.String(3), default='USD')
    source = db.Column(db.String(100))
    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    
    __table_args__ = (
        db.Index('idx_lithium_prices_date_compound_region', 'date', 'compound', 'region'),
    )
    
    def __repr__(self):
        return f'<LithiumPrice {self.compound} {self.region} {self.date}>'

class RelatedCommodityPrice(db.Model):
    """Model for related commodities prices (for correlation)"""
    __tablename__ = 'related_commodity_prices'
    
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, nullable=False)
    commodity = db.Column(db.String(50), nullable=False)  # cobalt, nickel, graphite, etc.
    price = db.Column(db.Float, nullable=False)
    currency = db.Column(db.String(3), default='USD')
    unit = db.Column(db.String(20), nullable=False)  # ton, kg, etc.
    source = db.Column(db.String(100))
    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    
    __table_args__ = (
        db.Index('idx_related_commodity_date_commodity', 'date', 'commodity'),
    )
    
    def __repr__(self):
        return f'<RelatedCommodityPrice {self.commodity} {self.date}>'

class PriceForecast(db.Model):
    """Model for lithium price forecasts"""
    __tablename__ = 'price_forecasts'
    
    id = db.Column(db.Integer, primary_key=True)
    created_date = db.Column(db.Date, nullable=False)
    forecast_date = db.Column(db.Date, nullable=False)
    compound = db.Column(db.String(50), nullable=False)
    region = db.Column(db.String(50), nullable=False)
    forecast_price = db.Column(db.Float, nullable=False)
    forecast_low = db.Column(db.Float)
    forecast_high = db.Column(db.Float)
    confidence = db.Column(db.Float)  # confidence level (0-1)
    model_name = db.Column(db.String(50))  # name of forecasting model
    
    __table_args__ = (
        db.Index('idx_price_forecasts_forecast_date_compound', 'forecast_date', 'compound'),
    )
    
    def __repr__(self):
        return f'<PriceForecast {self.compound} {self.forecast_date}>'
