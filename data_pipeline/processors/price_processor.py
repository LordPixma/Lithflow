# data_pipeline/processors/price_processor.py
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from app.models.price import LithiumPrice, PriceForecast
from app import db

class PriceProcessor:
    """Processor for lithium price data"""
    
    def __init__(self):
        pass
    
    def process_price_data(self, raw_data):
        """
        Process raw price data and save to database
        
        Args:
            raw_data: Dictionary with price data fields
        """
        try:
            # Create new price record
            price = LithiumPrice(
                date=raw_data.get('date'),
                compound=raw_data.get('compound'),
                grade=raw_data.get('grade'),
                region=raw_data.get('region'),
                price=raw_data.get('price'),
                price_low=raw_data.get('price_low'),
                price_high=raw_data.get('price_high'),
                currency=raw_data.get('currency', 'USD'),
                source=raw_data.get('source')
            )
            
            # Add to database
            db.session.add(price)
            db.session.commit()
            
            print(f"Saved price data: {price.compound} {price.region} {price.date}")
            return True
            
        except Exception as e:
            print(f"Error processing price data: {e}")
            db.session.rollback()
            return False
    
    def generate_price_forecast(self, compound, region, forecast_horizon=90):
        """
        Generate simple price forecast based on historical data
        
        Args:
            compound: Lithium compound type
            region: Geographic region
            forecast_horizon: Number of days to forecast
        """
        try:
            # Get historical data (last 180 days)
            end_date = datetime.now().date()
            start_date = end_date - timedelta(days=180)
            
            historical_prices = LithiumPrice.query.filter(
                LithiumPrice.compound == compound,
                LithiumPrice.region == region,
                LithiumPrice.date >= start_date,
                LithiumPrice.date <= end_date
            ).order_by(LithiumPrice.date).all()
            
            if not historical_prices:
                print(f"No historical data found for {compound} in {region}")
                return False
            
            # Convert to DataFrame for easier analysis
            df = pd.DataFrame([
                {
                    'date': price.date,
                    'price': price.price
                } for price in historical_prices
            ])
            
            # Simple moving average forecast (for MVP)
            # In a real implementation, more sophisticated models would be used
            last_price = df['price'].iloc[-1]
            avg_30d = df['price'].tail(30).mean()
            avg_90d = df['price'].tail(90).mean()
            
            # Calculate trend
            if len(df) >= 30:
                trend_30d = (df['price'].iloc[-1] - df['price'].iloc[-30]) / 30
            else:
                trend_30d = 0
            
            # Generate forecast dates
            forecast_dates = [end_date + timedelta(days=i) for i in range(1, forecast_horizon+1)]
            
            # Create forecast records
            forecasts = []
            for i, date in enumerate(forecast_dates):
                # Simple forecast model (last price + trend)
                forecast_price = last_price + (trend_30d * (i+1))
                
                # Add some volatility based on historical data
                if len(df) >= 30:
                    volatility = df['price'].tail(30).std()
                    forecast_low = forecast_price - volatility
                    forecast_high = forecast_price + volatility
                else:
                    # Default if not enough data
                    forecast_low = forecast_price * 0.95
                    forecast_high = forecast_price * 1.05
                
                # Create forecast record
                forecast = PriceForecast(
                    created_date=end_date,
                    forecast_date=date,
                    compound=compound,
                    region=region,
                    forecast_price=forecast_price,
                    forecast_low=forecast_low,
                    forecast_high=forecast_high,
                    confidence=0.7 - (i * 0.005),  # Lower confidence as we go further
                    model_name='SimpleTrend'
                )
                
                forecasts.append(forecast)
            
            # Save forecasts to database
            db.session.add_all(forecasts)
            db.session.commit()
            
            print(f"Generated {len(forecasts)} forecast points for {compound} in {region}")
            return True
            
        except Exception as e:
            print(f"Error generating price forecast: {e}")
            db.session.rollback()
            return False