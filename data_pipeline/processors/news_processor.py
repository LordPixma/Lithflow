# data_pipeline/processors/news_processor.py
import datetime
from app import db
from app.models.news import NewsArticle, NewsTag, NewsEntity

class NewsProcessor:
    """Processor for news data"""
    
    def __init__(self):
        pass
    
    def process_news_item(self, raw_data):
        """
        Process raw news item and save to database
        
        Args:
            raw_data: Dictionary with news item fields
        """
        try:
            # Check if article already exists by URL
            existing_article = NewsArticle.query.filter_by(url=raw_data.get('url')).first()
            
            if existing_article:
                # Update existing article
                existing_article.title = raw_data.get('title')
                existing_article.summary = raw_data.get('summary')
                existing_article.content = raw_data.get('content')
                existing_article.image_url = raw_data.get('image_url')
                existing_article.category = raw_data.get('category')
                existing_article.sentiment_score = raw_data.get('sentiment_score')
                existing_article.importance = raw_data.get('importance')
            else:
                # Create new article
                article = NewsArticle(
                    title=raw_data.get('title'),
                    url=raw_data.get('url'),
                    source=raw_data.get('source'),
                    published_date=raw_data.get('published_date'),
                    summary=raw_data.get('summary'),
                    content=raw_data.get('content'),
                    image_url=raw_data.get('image_url'),
                    category=raw_data.get('category'),
                    sentiment_score=raw_data.get('sentiment_score'),
                    importance=raw_data.get('importance')
                )
                db.session.add(article)
                db.session.flush()  # Get ID for new article
                
                # Add tags
                if 'tags' in raw_data and raw_data['tags']:
                    for tag in raw_data['tags']:
                        news_tag = NewsTag(article_id=article.id, tag=tag)
                        db.session.add(news_tag)
                
                # Add entities
                if 'entities' in raw_data and raw_data['entities']:
                    for entity in raw_data['entities']:
                        news_entity = NewsEntity(
                            article_id=article.id,
                            entity_name=entity.get('name'),
                            entity_type=entity.get('type')
                        )
                        db.session.add(news_entity)
            
            db.session.commit()
            return True
            
        except Exception as e:
            print(f"Error processing news item: {e}")
            db.session.rollback()
            return False