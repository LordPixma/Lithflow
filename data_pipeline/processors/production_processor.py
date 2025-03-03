# data_pipeline/processors/production_processor.py
import datetime
from app import db
from app.models.production import LithiumMine, MineProduction, ProcessingPlant, ProcessingProduction

class ProductionProcessor:
    """Processor for production data"""
    
    def __init__(self):
        pass
    
    def process_mine_production(self, raw_data):
        """
        Process raw mine production data and save to database
        
        Args:
            raw_data: Dictionary with production data fields
        """
        try:
            # Get mine from database or create if not exists
            mine = LithiumMine.query.filter_by(name=raw_data.get('mine_name')).first()
            
            if not mine:
                # Create new mine record if it doesn't exist
                mine = LithiumMine(
                    name=raw_data.get('mine_name'),
                    company=raw_data.get('company'),
                    country=raw_data.get('country'),
                    region=raw_data.get('region'),
                    type=raw_data.get('type'),
                    status=raw_data.get('status', 'operational'),
                    capacity=raw_data.get('capacity'),
                    start_year=raw_data.get('start_year'),
                    coordinates=raw_data.get('coordinates')
                )
                db.session.add(mine)
                db.session.commit()
            
            # Check if production record already exists
            existing_production = MineProduction.query.filter_by(
                mine_id=mine.id,
                year=raw_data.get('year'),
                quarter=raw_data.get('quarter')
            ).first()
            
            if existing_production:
                # Update existing record
                existing_production.production = raw_data.get('production')
                existing_production.grade = raw_data.get('grade')
                existing_production.cost = raw_data.get('cost')
                existing_production.source = raw_data.get('source')
                existing_production.is_estimate = raw_data.get('is_estimate', False)
            else:
                # Create new production record
                production = MineProduction(
                    mine_id=mine.id,
                    year=raw_data.get('year'),
                    quarter=raw_data.get('quarter'),
                    production=raw_data.get('production'),
                    grade=raw_data.get('grade'),
                    cost=raw_data.get('cost'),
                    source=raw_data.get('source'),
                    is_estimate=raw_data.get('is_estimate', False)
                )
                db.session.add(production)
            
            db.session.commit()
            print(f"Saved production data: {mine.name} {raw_data.get('year')} Q{raw_data.get('quarter')}")
            return True
            
        except Exception as e:
            print(f"Error processing production data: {e}")
            db.session.rollback()
            return False
    
    def process_plant_production(self, raw_data):
        """
        Process raw processing plant production data and save to database
        
        Args:
            raw_data: Dictionary with production data fields
        """
        try:
            # Similar implementation as process_mine_production but for processing plants
            # ...
            return True
            
        except Exception as e:
            print(f"Error processing plant production data: {e}")
            db.session.rollback()
            return False