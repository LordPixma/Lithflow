# data_pipeline/schedulers/scheduler.py
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from app import create_app, db
from data_pipeline.collectors.koyfin import KoyfinCollector
from data_pipeline.collectors.public_filings import PublicFilingsCollector
from data_pipeline.collectors.news_aggregator import NewsAggregator
from data_pipeline.processors.price_processor import PriceProcessor
from data_pipeline.processors.production_processor import ProductionProcessor
from data_pipeline.processors.news_processor import NewsProcessor
import datetime
import os

class DataPipelineScheduler:
    """Scheduler for data collection tasks"""
    
    def __init__(self, app=None):
        self.app = app or create_app()
        self.scheduler = BackgroundScheduler()
        
        # Initialize collectors and processors
        self.koyfin_collector = KoyfinCollector()
        self.filings_collector = PublicFilingsCollector()
        self.news_aggregator = NewsAggregator()
        
        self.price_processor = PriceProcessor()
        self.production_processor = ProductionProcessor()
        self.news_processor = NewsProcessor()
    
    def initialize_jobs(self):
        """Set up scheduled jobs"""
        # Daily price data collection - every day at 1 AM
        self.scheduler.add_job(
            self.collect_price_data,
            CronTrigger(hour=1, minute=0),
            id='collect_price_data',
            replace_existing=True
        )
        
        # Weekly production data update - every Monday at 2 AM
        self.scheduler.add_job(
            self.collect_production_data,
            CronTrigger(day_of_week='mon', hour=2, minute=0),
            id='collect_production_data',
            replace_existing=True
        )
        
        # News collection - every 6 hours
        self.scheduler.add_job(
            self.collect_news,
            CronTrigger(hour='*/6', minute=30),
            id='collect_news',
            replace_existing=True
        )
        
        # Price forecasting - every Sunday at 3 AM
        self.scheduler.add_job(
            self.update_price_forecasts,
            CronTrigger(day_of_week='sun', hour=3, minute=0),
            id='update_price_forecasts',
            replace_existing=True
        )
    
    def start(self):
        """Start the scheduler"""
        self.initialize_jobs()
        self.scheduler.start()
        print("Data pipeline scheduler started")
    
    def shutdown(self):
        """Shutdown the scheduler"""
        self.scheduler.shutdown()
        print("Data pipeline scheduler stopped")
    
    def collect_price_data(self):
        """Job to collect daily price data"""
        with self.app.app_context():
            print(f"Starting price data collection: {datetime.datetime.now()}")
            
            # In a real implementation, this would fetch from actual sources
            # For MVP, we'll simulate some data
            compounds = ['lithium carbonate', 'lithium hydroxide']
            regions = ['China', 'US', 'Europe', 'South America']
            
            for compound in compounds:
                for region in regions:
                    # Simulate price data
                    raw_data = {
                        'date': datetime.datetime.now().date(),
                        'compound': compound,
                        'grade': 'battery',
                        'region': region,
                        'price': 15000 + (region == 'China') * 2000 + (compound == 'lithium hydroxide') * 3000,
                        'price_low': 14500 + (region == 'China') * 1800 + (compound == 'lithium hydroxide') * 2800,
                        'price_high': 15500 + (region == 'China') * 2200 + (compound == 'lithium hydroxide') * 3200,
                        'currency': 'USD',
                        'source': 'Simulated Data'
                    }
                    
                    # Process and save data
                    self.price_processor.process_price_data(raw_data)
            
            print(f"Completed price data collection: {datetime.datetime.now()}")
    
    def collect_production_data(self):
        """Job to collect weekly production data updates"""
        with self.app.app_context():
            print(f"Starting production data collection: {datetime.datetime.now()}")
            
            # In a real implementation, this would fetch from actual sources
            # For MVP, we'll simulate some data
            # Implementation would be similar to price data collection
            
            print(f"Completed production data collection: {datetime.datetime.now()}")
    
    def collect_news(self):
        """Job to collect news articles"""
        with self.app.app_context():
            print(f"Starting news collection: {datetime.datetime.now()}")
            
            # Fetch news from all sources
            news_items = self.news_aggregator.fetch_all_sources()
            
            # Process and save each news item
            for item in news_items:
                self.news_processor.process_news_item(item)
            
            print(f"Completed news collection: {datetime.datetime.now()}")
    
    def update_price_forecasts(self):
        """Job to update price forecasts"""
        with self.app.app_context():
            print(f"Starting price forecast update: {datetime.datetime.now()}")
            
            # Get distinct compound-region combinations
            compounds = db.session.query(db.distinct(LithiumPrice.compound)).all()
            regions = db.session.query(db.distinct(LithiumPrice.region)).all()
            
            for compound in [c[0] for c in compounds]:
                for region in [r[0] for r in regions]:
                    self.price_processor.generate_price_forecast(compound, region)
            
            print(f"Completed price forecast update: {datetime.datetime.now()}")

# Initialize and run scheduler (for production deployment)
def run_scheduler():
    scheduler = DataPipelineScheduler()
    scheduler.start()
    
    try:
        # Keep the main thread alive
        while True:
            pass
    except (KeyboardInterrupt, SystemExit):
        scheduler.shutdown()

if __name__ == '__main__':
    run_scheduler()