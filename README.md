# LithFlow: Global Lithium Market Intelligence Platform

LithFlow is a comprehensive market intelligence platform designed to provide real-time insights into the global lithium industry. From mining and production to pricing and market trends, LithFlow delivers actionable data and analytics for industry professionals, investors, and analysts.

![LithFlow Dashboard Screenshot](docs/images/dashboard-screenshot.png)

## Features

### Price Intelligence
- Real-time and historical lithium compound price tracking
- Regional price comparisons (China, US, Europe, South America)
- Price correlation with related commodities
- Advanced price forecasting models (Premium)

### Production Tracking
- Mine-level production volume monitoring
- Country and company production dashboards
- Processing and refining capacity tracking
- Project pipeline visualization and status updates (Premium)

### Market Analytics
- Supply-demand balance modeling
- EV market penetration tracking
- Battery chemistry trends analysis (Premium)
- Regulatory impact assessment (Premium)
- Trade flow visualization (Premium)

### News & Research
- Curated news aggregation service
- Company announcement tracking
- Research report summaries
- Sentiment analysis on market news (Premium)
- Custom alert system

### User Management
- Tiered access control (Basic vs. Premium)
- Customizable dashboards and preferences
- Personalized data export capabilities
- Custom alert configuration

## Tech Stack

- **Backend**: Flask (Python)
- **Database**: PostgreSQL with TimescaleDB extension
- **Frontend**: HTML, CSS, JavaScript with Jinja2 templates
- **Data Visualization**: Chart.js, D3.js
- **Data Processing**: Pandas, NumPy
- **Containerization**: Docker, Docker Compose
- **Task Scheduling**: APScheduler
- **Web Server**: Gunicorn behind Nginx
- **Authentication**: Flask-Login, WTForms
- **CSS Framework**: Bootstrap 5
- **Version Control**: Git
- **Testing**: Pytest

## Installation

### Prerequisites
- Python 3.9+
- PostgreSQL 14+ with TimescaleDB extension
- Redis (for task scheduling)
- Git

### Local Development Setup

1. Clone the repository:
```bash
git clone https://github.com/yourusername/lithflow.git
cd lithflow
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Create PostgreSQL database:
```bash
createdb lithflow
```

5. Set environment variables (or create a `.env` file):
```bash
export FLASK_APP=run.py
export FLASK_ENV=development
export DATABASE_URL=postgresql://username:password@localhost:5432/lithflow
export SECRET_KEY=your-secure-secret-key
```

6. Initialize the database:
```bash
flask db upgrade
python init_db.py
```

7. Run the development server:
```bash
flask run
```

8. Start the data pipeline in a separate terminal:
```bash
python -m data_pipeline.schedulers.scheduler
```

### Docker Setup

1. Clone the repository:
```bash
git clone https://github.com/yourusername/lithflow.git
cd lithflow
```

2. Create a `.env` file with the following variables:
```
SECRET_KEY=your-secure-secret-key
```

3. Build and start the containers:
```bash
docker-compose up -d
```

4. Initialize the database:
```bash
docker-compose exec web flask db upgrade
docker-compose exec web python init_db.py
```

The application will be available at http://localhost:5000

## Production Deployment

For production deployment, we recommend using:
- Gunicorn as WSGI server
- Nginx as reverse proxy
- Supervisor to manage processes
- PostgreSQL with TimescaleDB extension
- SSL/TLS certificate for secure connections

Follow these steps:

1. Set up a Linux server (Ubuntu/Debian recommended)
2. Clone the repository to `/opt/lithflow`
3. Run the installation script:
```bash
cd /opt/lithflow
sudo ./deployment/install.sh
```

4. Configure your domain by updating the Nginx configuration in `/etc/nginx/sites-available/lithflow`
5. Obtain SSL certificate (we recommend Let's Encrypt):
```bash
sudo certbot --nginx -d yourdomain.com
```

6. Restart Nginx:
```bash
sudo systemctl restart nginx
```

For detailed deployment instructions, see [DEPLOYMENT.md](docs/DEPLOYMENT.md).

## Project Structure

```
lithflow/
├── app/                          # Main application code
│   ├── __init__.py               # Flask application factory
│   ├── config.py                 # Configuration settings
│   ├── models/                   # SQLAlchemy models
│   ├── blueprints/               # Flask blueprints (modules)
│   ├── static/                   # Static assets
│   ├── templates/                # Jinja templates
│   └── utils/                    # Utility functions
├── data_pipeline/                # Data collection & ETL
│   ├── collectors/               # Data source collectors
│   ├── processors/               # Data processors
│   ├── schedulers/               # Job schedulers
│   └── models/                   # ETL data models
├── tests/                        # Test suite
├── migrations/                   # Database migrations
├── deployment/                   # Deployment scripts
├── docker-compose.yml            # Docker Compose configuration
├── Dockerfile                    # Docker build file
├── requirements.txt              # Python dependencies
├── run.py                        # Application entry point
└── init_db.py                    # Database initialization script
```

## Development Workflow

### Code Style
We follow PEP 8 Python coding standards. Please ensure your code conforms to these standards.

### Database Migrations
When making changes to models, create and apply migrations:
```bash
flask db migrate -m "Description of changes"
flask db upgrade
```

### Running Tests
To run the test suite:
```bash
pytest
```

For coverage report:
```bash
pytest --cov=app tests/
```

### Adding Data Sources
To add a new data source:
1. Create a new collector class in `data_pipeline/collectors/`
2. Implement the required methods for data extraction
3. Update the ETL scheduler as needed
4. Create a processor for the data if necessary

## API Documentation

LithFlow offers internal API endpoints for the frontend. These are not intended for external use but are documented for development purposes.

### Price Intelligence
- `GET /prices/api/price-data` - Get price data for charting
- `GET /prices/api/forecast-data` - Get price forecast data (Premium)

### Production Tracking
- `GET /production/api/mine-data` - Get mine production data
- `GET /production/api/country-production` - Get country-level production
- `GET /production/api/project-timeline` - Get project development timeline

### Market Analytics
- `GET /market/api/supply-demand-data` - Get supply-demand balance data
- `GET /market/api/ev-market-data` - Get EV market data
- `GET /market/api/battery-chemistry-data` - Get battery chemistry data
- `GET /market/api/regulation-events` - Get regulatory events
- `GET /market/api/trade-flow-data` - Get trade flow data

### News
- `GET /news/api/latest-news` - Get latest news articles
- `GET /news/api/search-news` - Search news articles
- `GET /news/api/company-announcements` - Get company announcements
- `GET /news/api/research-reports` - Get research reports
- `GET /news/api/sentiment-data` - Get sentiment analysis data

For detailed API documentation, see [API.md](docs/API.md).

## User Guide

### Creating an Account
1. Navigate to the LithFlow login page
2. Click on "Create Account"
3. Fill in your details and submit the registration form
4. Verify your email address (if enabled)
5. Log in with your new credentials

### Setting Up Alerts
1. Navigate to the Alerts page from your user profile
2. Click "Add New Alert"
3. Choose alert type (price threshold, news keyword, etc.)
4. Configure alert parameters and frequency
5. Save your alert settings

### Customizing Your Dashboard
1. Go to user preferences
2. Select your default dashboard view
3. Configure display preferences
4. Set up chart color themes
5. Save your preferences

For more detailed usage instructions, see [USER_GUIDE.md](docs/USER_GUIDE.md).

## Contributing

We welcome contributions to LithFlow! Please follow these steps to contribute:

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/your-feature-name`
3. Make your changes and commit them
4. Push to your branch: `git push origin feature/your-feature-name`
5. Create a Pull Request

For more details, see [CONTRIBUTING.md](docs/CONTRIBUTING.md).

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contact

For questions, support, or feedback, please contact:
- Email: support@lithflow.com
- Website: https://www.lithflow.com

## Acknowledgments

- Data providers and industry partners
- Open source libraries and tools used in this project
- Contributors who have helped build and improve LithFlow