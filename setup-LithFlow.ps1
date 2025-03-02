# PowerShell script to create the LithFlow application structure
# Run this script from the folder where you want the lithflow project to be created

# Create main project directory
New-Item -ItemType Directory -Path "lithflow" | Out-Null
Set-Location -Path "lithflow"

# Create app directory structure
$directories = @(
    "app",
    "app/models",
    "app/blueprints",
    "app/blueprints/auth",
    "app/blueprints/prices",
    "app/blueprints/production",
    "app/blueprints/market_analytics",
    "app/blueprints/news",
    "app/blueprints/user",
    "app/static",
    "app/static/css",
    "app/static/js",
    "app/static/images",
    "app/templates",
    "app/templates/auth",
    "app/templates/dashboard",
    "app/templates/prices",
    "app/templates/production",
    "app/templates/market",
    "app/templates/news",
    "app/templates/user",
    "app/utils",
    "data_pipeline",
    "data_pipeline/collectors",
    "data_pipeline/processors",
    "data_pipeline/schedulers",
    "data_pipeline/models",
    "tests",
    "migrations"
)

foreach ($dir in $directories) {
    New-Item -ItemType Directory -Path $dir | Out-Null
    Write-Host "Created directory: $dir"
}

# Create app/__init__.py
$initPyContent = @"
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager

# Initialize extensions
db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()

def create_app(config_name='default'):
    """Create and configure the Flask application"""
    app = Flask(__name__)
    # Configure app here
    return app
"@
Set-Content -Path "app/__init__.py" -Value $initPyContent
Write-Host "Created file: app/__init__.py"

# Create app/config.py
$configPyContent = @"
import os

class Config:
    """Base configuration"""
    SECRET_KEY = os.environ.get('SECRET_KEY', 'dev-key-for-development')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', 'postgresql://postgres:postgres@localhost:5432/lithflow')

class DevelopmentConfig(Config):
    """Development configuration"""
    DEBUG = True

class ProductionConfig(Config):
    """Production configuration"""
    DEBUG = False

config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
"@
Set-Content -Path "app/config.py" -Value $configPyContent
Write-Host "Created file: app/config.py"

# Create app/extensions.py
Set-Content -Path "app/extensions.py" -Value "# Flask extensions initialization"
Write-Host "Created file: app/extensions.py"

# Create app/commands.py
Set-Content -Path "app/commands.py" -Value "# CLI commands"
Write-Host "Created file: app/commands.py"

# Create model files
$modelFiles = @(
    "app/models/__init__.py",
    "app/models/user.py",
    "app/models/price.py",
    "app/models/production.py",
    "app/models/news.py",
    "app/models/market.py"
)

foreach ($file in $modelFiles) {
    New-Item -ItemType File -Path $file | Out-Null
    Write-Host "Created file: $file"
}

# Create blueprint files
$blueprints = @("auth", "prices", "production", "market_analytics", "news", "user")

foreach ($blueprint in $blueprints) {
    $blueprintInitContent = @"
from flask import Blueprint

${blueprint}_bp = Blueprint('$blueprint', __name__, url_prefix='/$blueprint')

from . import routes
"@
    Set-Content -Path "app/blueprints/$blueprint/__init__.py" -Value $blueprintInitContent
    New-Item -ItemType File -Path "app/blueprints/$blueprint/routes.py" | Out-Null
    if ($blueprint -eq "auth") {
        New-Item -ItemType File -Path "app/blueprints/$blueprint/forms.py" | Out-Null
    }
    Write-Host "Created blueprint files for: $blueprint"
}

# Create utilities
$utilFiles = @(
    "app/utils/__init__.py",
    "app/utils/helpers.py",
    "app/utils/decorators.py",
    "app/utils/error_handlers.py"
)

foreach ($file in $utilFiles) {
    New-Item -ItemType File -Path $file | Out-Null
    Write-Host "Created file: $file"
}

# Create data pipeline files
$pipelineFiles = @(
    "data_pipeline/__init__.py",
    "data_pipeline/collectors/__init__.py",
    "data_pipeline/processors/__init__.py",
    "data_pipeline/schedulers/__init__.py",
    "data_pipeline/models/__init__.py",
    "data_pipeline/collectors/koyfin.py",
    "data_pipeline/collectors/public_filings.py",
    "data_pipeline/collectors/government_data.py",
    "data_pipeline/collectors/news_aggregator.py",
    "data_pipeline/processors/price_processor.py",
    "data_pipeline/processors/production_processor.py",
    "data_pipeline/processors/news_processor.py",
    "data_pipeline/schedulers/scheduler.py",
    "data_pipeline/models/raw_data.py"
)

foreach ($file in $pipelineFiles) {
    New-Item -ItemType File -Path $file | Out-Null
    Write-Host "Created file: $file"
}

# Create test files
$testFiles = @(
    "tests/__init__.py",
    "tests/conftest.py",
    "tests/test_auth.py",
    "tests/test_prices.py",
    "tests/test_production.py"
)

foreach ($file in $testFiles) {
    New-Item -ItemType File -Path $file | Out-Null
    Write-Host "Created file: $file"
}

# Create templates
$templateFiles = @(
    "app/templates/base.html",
    "app/templates/auth/login.html",
    "app/templates/auth/register.html",
    "app/templates/dashboard/index.html",
    "app/templates/prices/dashboard.html",
    "app/templates/prices/regional_comparison.html",
    "app/templates/production/mine_dashboard.html",
    "app/templates/production/processing_dashboard.html",
    "app/templates/market/supply_demand.html"
)

foreach ($file in $templateFiles) {
    New-Item -ItemType File -Path $file | Out-Null
    Write-Host "Created file: $file"
}

# Create static files
$staticFiles = @(
    "app/static/css/style.css",
    "app/static/js/main.js"
)

foreach ($file in $staticFiles) {
    New-Item -ItemType File -Path $file | Out-Null
    Write-Host "Created file: $file"
}

# Create run.py
$runPyContent = @"
from app import create_app

app = create_app()

if __name__ == '__main__':
    app.run(debug=True)
"@
Set-Content -Path "run.py" -Value $runPyContent
Write-Host "Created file: run.py"

# Create requirements.txt
$requirementsContent = @"
Flask==2.3.3
flask-sqlalchemy==3.1.1
flask-migrate==4.0.5
flask-login==0.6.3
flask-wtf==1.2.1
WTForms==3.1.1
psycopg2-binary==2.9.9
requests==2.31.0
beautifulsoup4==4.12.2
pandas==2.1.1
numpy==1.26.0
apscheduler==3.10.4
python-dotenv==1.0.0
"@
Set-Content -Path "requirements.txt" -Value $requirementsContent
Write-Host "Created file: requirements.txt"

# Create .env
$envContent = @"
SECRET_KEY=development-key
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/lithflow
FLASK_APP=run.py
FLASK_ENV=development
"@
Set-Content -Path ".env" -Value $envContent
Write-Host "Created file: .env"

# Create .gitignore
$gitignoreContent = @"
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
venv/
ENV/
env.bak/
venv.bak/
.env

# Flask
instance/
.webassets-cache

# PyCharm
.idea/

# VS Code
.vscode/

# Database
*.db
*.sqlite

# Logs
*.log

# Distribution / packaging
dist/
build/
*.egg-info/
"@
Set-Content -Path ".gitignore" -Value $gitignoreContent
Write-Host "Created file: .gitignore"

# Create README.md
$readmeContent = @"
# LithFlow: Global Lithium Market Intelligence Platform

LithFlow is a SaaS platform providing comprehensive market intelligence for the global lithium industry. The platform aggregates, analyzes, and visualizes data across the lithium value chain - from mining and processing to battery manufacturing and end-use markets.

## Installation

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```
"@
Set-Content -Path "README.md" -Value $readmeContent
Write-Host "Created file: README.md"

Write-Host "`nProject structure created successfully!`n"
Write-Host "Next steps:"
Write-Host "1. Create a PostgreSQL database named 'lithflow'"
Write-Host "2. Activate your virtual environment: venv\Scripts\activate"
Write-Host "3. Install dependencies: pip install -r requirements.txt"
Write-Host "4. Initialize database: flask db init"
Write-Host "5. Run the application: python run.py"