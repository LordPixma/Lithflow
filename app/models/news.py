# app/models/news.py
from app import db
import datetime

class NewsArticle(db.Model):
    """Model for lithium industry news articles"""
    __tablename__ = 'news_articles'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    url = db.Column(db.String(500), nullable=False)
    source = db.Column(db.String(100), nullable=False)
    published_date = db.Column(db.DateTime, nullable=False)
    summary = db.Column(db.Text)
    content = db.Column(db.Text)
    image_url = db.Column(db.String(500))
    category = db.Column(db.String(50))  # market, production, technology, regulation, etc.
    sentiment_score = db.Column(db.Float)  # -1.0 to 1.0 scale
    importance = db.Column(db.Integer)  # 1-10 scale
    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    
    # Relationships
    tags = db.relationship('NewsTag', backref='article', lazy=True, cascade='all, delete-orphan')
    entities = db.relationship('NewsEntity', backref='article', lazy=True, cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<NewsArticle {self.title[:30]}...>'

class NewsTag(db.Model):
    """Model for news article tags"""
    __tablename__ = 'news_tags'
    
    id = db.Column(db.Integer, primary_key=True)
    article_id = db.Column(db.Integer, db.ForeignKey('news_articles.id'), nullable=False)
    tag = db.Column(db.String(50), nullable=False)
    
    def __repr__(self):
        return f'<NewsTag {self.tag}>'

class NewsEntity(db.Model):
    """Model for named entities in news articles"""
    __tablename__ = 'news_entities'
    
    id = db.Column(db.Integer, primary_key=True)
    article_id = db.Column(db.Integer, db.ForeignKey('news_articles.id'), nullable=False)
    entity_name = db.Column(db.String(100), nullable=False)
    entity_type = db.Column(db.String(50), nullable=False)  # company, person, location, etc.
    
    def __repr__(self):
        return f'<NewsEntity {self.entity_name} ({self.entity_type})>'

class ResearchReport(db.Model):
    """Model for research reports and analyst notes"""
    __tablename__ = 'research_reports'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    publisher = db.Column(db.String(100), nullable=False)
    published_date = db.Column(db.Date, nullable=False)
    summary = db.Column(db.Text)
    file_path = db.Column(db.String(500))  # path to PDF or document
    key_findings = db.Column(db.Text)
    is_premium = db.Column(db.Boolean, default=True)  # require premium access
    source = db.Column(db.String(100))
    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    
    def __repr__(self):
        return f'<ResearchReport {self.title[:30]}...>'

class CompanyAnnouncement(db.Model):
    """Model for lithium company announcements"""
    __tablename__ = 'company_announcements'
    
    id = db.Column(db.Integer, primary_key=True)
    company = db.Column(db.String(100), nullable=False)
    announcement_date = db.Column(db.Date, nullable=False)
    title = db.Column(db.String(255), nullable=False)
    url = db.Column(db.String(500))
    announcement_type = db.Column(db.String(50))  # production, financial, project, etc.
    summary = db.Column(db.Text)
    importance = db.Column(db.Integer)  # 1-10 scale
    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    
    def __repr__(self):
        return f'<CompanyAnnouncement {self.company} {self.announcement_date}>'