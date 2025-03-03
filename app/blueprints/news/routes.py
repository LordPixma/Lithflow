# app/blueprints/news/routes.py
from flask import render_template, jsonify, request, redirect, url_for
from flask_login import login_required, current_user
from app.blueprints.news import news_bp
from app.models.news import (
    NewsArticle, NewsTag, NewsEntity, ResearchReport, 
    CompanyAnnouncement
)
from app.utils.access_control import premium_required
from app import db
from sqlalchemy import func, desc
import datetime

@news_bp.route('/latest')
@login_required
def latest():
    """View for latest news articles"""
    categories = db.session.query(NewsArticle.category).distinct().all()
    
    return render_template(
        'news/latest.html',
        categories=[c[0] for c in categories if c[0] is not None]
    )

@news_bp.route('/api/latest-news')
@login_required
def latest_news_data():
    """API endpoint to get latest news data"""
    category = request.args.get('category', None)
    days = request.args.get('days', 7)
    limit = request.args.get('limit', 20)
    
    # Calculate date range
    end_date = datetime.datetime.now()
    start_date = end_date - datetime.timedelta(days=int(days))
    
    # Build filter
    filters = [
        NewsArticle.published_date >= start_date,
        NewsArticle.published_date <= end_date
    ]
    
    if category and category != 'all':
        filters.append(NewsArticle.category == category)
    
    # Query data
    articles = NewsArticle.query.filter(
        *filters
    ).order_by(
        NewsArticle.published_date.desc()
    ).limit(int(limit)).all()
    
    # Format for response
    result = []
    for article in articles:
        # Get tags for this article
        tags = [tag.tag for tag in article.tags]
        
        # Get entities for this article
        entities = [{
            'name': entity.entity_name,
            'type': entity.entity_type
        } for entity in article.entities]
        
        article_data = {
            'id': article.id,
            'title': article.title,
            'url': article.url,
            'source': article.source,
            'published_date': article.published_date.strftime('%Y-%m-%d %H:%M'),
            'summary': article.summary,
            'image_url': article.image_url,
            'category': article.category,
            'sentiment_score': article.sentiment_score,
            'importance': article.importance,
            'tags': tags,
            'entities': entities
        }
        
        result.append(article_data)
    
    return jsonify(result)

@news_bp.route('/search')
@login_required
def search():
    """View for news search"""
    return render_template('news/search.html')

@news_bp.route('/api/search-news')
@login_required
def search_news():
    """API endpoint to search news articles"""
    query = request.args.get('query', '')
    start_date = request.args.get('start_date', None)
    end_date = request.args.get('end_date', None)
    source = request.args.get('source', None)
    limit = request.args.get('limit', 50)
    
    # Build filter
    filters = []
    
    if query:
        filters.append(NewsArticle.title.ilike(f'%{query}%') | 
                        NewsArticle.summary.ilike(f'%{query}%'))
    
    if start_date:
        start_date = datetime.datetime.strptime(start_date, '%Y-%m-%d')
        filters.append(NewsArticle.published_date >= start_date)
    
    if end_date:
        end_date = datetime.datetime.strptime(end_date, '%Y-%m-%d')
        filters.append(NewsArticle.published_date <= end_date)
    
    if source:
        filters.append(NewsArticle.source == source)
    
    # Query data
    articles = NewsArticle.query.filter(
        *filters
    ).order_by(
        NewsArticle.published_date.desc()
    ).limit(int(limit)).all()
    
    # Format for response (similar to latest-news)
    result = []
    for article in articles:
        article_data = {
            'id': article.id,
            'title': article.title,
            'url': article.url,
            'source': article.source,
            'published_date': article.published_date.strftime('%Y-%m-%d %H:%M'),
            'summary': article.summary,
            'category': article.category,
            'sentiment_score': article.sentiment_score,
        }
        
        result.append(article_data)
    
    return jsonify(result)

@news_bp.route('/company-announcements')
@login_required
def company_announcements():
    """View for company announcements"""
    companies = db.session.query(CompanyAnnouncement.company).distinct().all()
    types = db.session.query(CompanyAnnouncement.announcement_type).distinct().all()
    
    return render_template(
        'news/company_announcements.html',
        companies=[c[0] for c in companies],
        types=[t[0] for t in types if t[0] is not None]
    )

@news_bp.route('/api/company-announcements')
@login_required
def company_announcements_data():
    """API endpoint to get company announcements"""
    company = request.args.get('company', None)
    announcement_type = request.args.get('type', None)
    limit = request.args.get('limit', 20)
    
    # Build filter
    filters = []
    
    if company:
        filters.append(CompanyAnnouncement.company == company)
    
    if announcement_type:
        filters.append(CompanyAnnouncement.announcement_type == announcement_type)
    
    # Query data
    announcements = CompanyAnnouncement.query.filter(
        *filters
    ).order_by(
        CompanyAnnouncement.announcement_date.desc()
    ).limit(int(limit)).all()
    
    # Format for response
    result = [{
        'id': announcement.id,
        'company': announcement.company,
        'announcement_date': announcement.announcement_date.strftime('%Y-%m-%d'),
        'title': announcement.title,
        'url': announcement.url,
        'announcement_type': announcement.announcement_type,
        'summary': announcement.summary,
        'importance': announcement.importance
    } for announcement in announcements]
    
    return jsonify(result)

@news_bp.route('/research-reports')
@login_required
def research_reports():
    """View for research reports"""
    publishers = db.session.query(ResearchReport.publisher).distinct().all()
    
    return render_template(
        'news/research_reports.html',
        publishers=[p[0] for p in publishers]
    )

@news_bp.route('/api/research-reports')
@login_required
def research_reports_data():
    """API endpoint to get research reports"""
    publisher = request.args.get('publisher', None)
    limit = request.args.get('limit', 10)
    
    # Build filter
    filters = []
    
    if publisher:
        filters.append(ResearchReport.publisher == publisher)
    
    # If user is not premium, only show non-premium reports
    if not current_user.is_premium():
        filters.append(ResearchReport.is_premium == False)
    
    # Query data
    reports = ResearchReport.query.filter(
        *filters
    ).order_by(
        ResearchReport.published_date.desc()
    ).limit(int(limit)).all()
    
    # Format for response
    result = [{
        'id': report.id,
        'title': report.title,
        'publisher': report.publisher,
        'published_date': report.published_date.strftime('%Y-%m-%d'),
        'summary': report.summary,
        'file_path': report.file_path if current_user.is_premium() or not report.is_premium else None,
        'is_premium': report.is_premium
    } for report in reports]
    
    return jsonify(result)

@news_bp.route('/report/<int:report_id>')
@login_required
def view_report(report_id):
    """View a specific research report"""
    report = ResearchReport.query.get_or_404(report_id)
    
    # Check access for premium reports
    if report.is_premium and not current_user.is_premium():
        return render_template('news/premium_required.html')
    
    return render_template(
        'news/view_report.html',
        report=report
    )

@news_bp.route('/market-sentiment')
@login_required
@premium_required
def market_sentiment():
    """View for market sentiment analysis (premium)"""
    return render_template('news/market_sentiment.html')

@news_bp.route('/api/sentiment-data')
@login_required
@premium_required
def sentiment_data():
    """API endpoint to get sentiment analysis data"""
    days = request.args.get('days', 30)
    
    # Calculate date range
    end_date = datetime.datetime.now()
    start_date = end_date - datetime.timedelta(days=int(days))
    
    # Get daily average sentiment
    sentiment_by_day = db.session.query(
        func.date(NewsArticle.published_date).label('date'),
        func.avg(NewsArticle.sentiment_score).label('avg_sentiment'),
        func.count(NewsArticle.id).label('article_count')
    ).filter(
        NewsArticle.published_date >= start_date,
        NewsArticle.published_date <= end_date,
        NewsArticle.sentiment_score.isnot(None)
    ).group_by(
        func.date(NewsArticle.published_date)
    ).order_by(
        func.date(NewsArticle.published_date)
    ).all()
    
    # Format for response
    sentiment_data = [{
        'date': day.date.strftime('%Y-%m-%d'),
        'sentiment': day.avg_sentiment,
        'article_count': day.article_count
    } for day in sentiment_by_day]
    
    # Get sentiment by category
    sentiment_by_category = db.session.query(
        NewsArticle.category,
        func.avg(NewsArticle.sentiment_score).label('avg_sentiment'),
        func.count(NewsArticle.id).label('article_count')
    ).filter(
        NewsArticle.published_date >= start_date,
        NewsArticle.published_date <= end_date,
        NewsArticle.sentiment_score.isnot(None),
        NewsArticle.category.isnot(None)
    ).group_by(
        NewsArticle.category
    ).all()
    
    # Format for response
    category_data = [{
        'category': cat.category,
        'sentiment': cat.avg_sentiment,
        'article_count': cat.article_count
    } for cat in sentiment_by_category]
    
    # Get most positive and negative articles
    positive_articles = NewsArticle.query.filter(
        NewsArticle.published_date >= start_date,
        NewsArticle.published_date <= end_date,
        NewsArticle.sentiment_score.isnot(None)
    ).order_by(
        NewsArticle.sentiment_score.desc()
    ).limit(5).all()
    
    negative_articles = NewsArticle.query.filter(
        NewsArticle.published_date >= start_date,
        NewsArticle.published_date <= end_date,
        NewsArticle.sentiment_score.isnot(None)
    ).order_by(
        NewsArticle.sentiment_score.asc()
    ).limit(5).all()
    
    # Format articles
    positive_data = [{
        'title': article.title,
        'source': article.source,
        'date': article.published_date.strftime('%Y-%m-%d'),
        'sentiment': article.sentiment_score
    } for article in positive_articles]
    
    negative_data = [{
        'title': article.title,
        'source': article.source,
        'date': article.published_date.strftime('%Y-%m-%d'),
        'sentiment': article.sentiment_score
    } for article in negative_articles]
    
    result = {
        'daily_sentiment': sentiment_data,
        'category_sentiment': category_data,
        'most_positive': positive_data,
        'most_negative': negative_data
    }
    
    return jsonify(result)