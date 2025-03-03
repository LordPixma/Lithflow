# tests/conftest.py
import os
import tempfile
import pytest
from app import create_app, db
from app.models.user import User
from app.models.price import LithiumPrice
from app.models.production import LithiumMine, MineProduction
from datetime import datetime, timedelta

@pytest.fixture
def app():
    """Create and configure a Flask app for testing"""
    # Create a temporary file to isolate the database for each test
    db_fd, db_path = tempfile.mkstemp()
    
    app = create_app('testing')
    app.config.update({
        'SQLALCHEMY_DATABASE_URI': f'sqlite:///{db_path}',
        'WTF_CSRF_ENABLED': False,
        'TESTING': True
    })
    
    # Create the database and load test data
    with app.app_context():
        db.create_all()
        _load_test_data()
    
    yield app
    
    # Close and remove the temporary database
    os.close(db_fd)
    os.unlink(db_path)

@pytest.fixture
def client(app):
    """A test client for the app"""
    return app.test_client()

@pytest.fixture
def runner(app):
    """A test CLI runner for the app"""
    return app.test_cli_runner()

@pytest.fixture
def auth(client):
    """Authentication helper for tests"""
    class AuthActions:
        def login(self, email='user@example.com', password='userpassword'):
            return client.post(
                '/auth/login',
                data={'email': email, 'password': password}
            )
        
        def logout(self):
            return client.get('/auth/logout')
    
    return AuthActions()

def _load_test_data():
    """Load test data into the database"""
    # Create test users
    admin = User(
        username="admin",
        email="admin@example.com",
        company="TestCorp",
        role="admin",
        created_at=datetime.now(),
        last_login=datetime.now()
    )
    admin.password = "adminpassword"
    
    premium = User(
        username="premium",
        email="premium@example.com",
        company="PremiumCorp",
        role="premium",
        created_at=datetime.now(),
        last_login=datetime.now()
    )
    premium.password = "premiumpassword"
    
    user = User(
        username="user",
        email="user@example.com",
        company="BasicCorp",
        role="basic",
        created_at=datetime.now(),
        last_login=datetime.now()
    )
    user.password = "userpassword"
    
    db.session.add_all([admin, premium, user])
    
    # Create test price data
    today = datetime.now().date()
    yesterday = today - timedelta(days=1)
    
    price1 = LithiumPrice(
        date=today,
        compound="lithium carbonate",
        grade="battery",
        region="China",
        price=25000.0,
        price_low=24000.0,
        price_high=26000.0,
        currency="USD",
        source="Test Data"
    )
    
    price2 = LithiumPrice(
        date=yesterday,
        compound="lithium carbonate",
        grade="battery",
        region="China",
        price=25500.0,
        price_low=24500.0,
        price_high=26500.0,
        currency="USD",
        source="Test Data"
    )
    
    price3 = LithiumPrice(
        date=today,
        compound="lithium hydroxide",
        grade="battery",
        region="China",
        price=30000.0,
        price_low=29000.0,
        price_high=31000.0,
        currency="USD",
        source="Test Data"
    )
    
    db.session.add_all([price1, price2, price3])
    
    # Create test production data
    mine1 = LithiumMine(
        name="Test Mine 1",
        company="Test Mining Co",
        country="Australia",
        region="Oceania",
        type="hard rock",
        status="operational",
        capacity=100000,
        start_year=2020,
        coordinates="-33.8667,115.9833"
    )
    
    mine2 = LithiumMine(
        name="Test Mine 2",
        company="Test Lithium",
        country="Chile",
        region="South America",
        type="brine",
        status="operational",
        capacity=50000,
        start_year=2018,
        coordinates="-23.5000,-68.0000"
    )
    
    db.session.add_all([mine1, mine2])
    db.session.commit()
    
    # Add production data
    production1 = MineProduction(
        mine_id=mine1.id,
        year=datetime.now().year,
        quarter=None,  # Annual data
        production=80000,
        grade=1.8,
        cost=4500,
        source="Test Data",
        is_estimate=False
    )
    
    production2 = MineProduction(
        mine_id=mine2.id,
        year=datetime.now().year,
        quarter=None,  # Annual data
        production=40000,
        grade=0.15,
        cost=3800,
        source="Test Data",
        is_estimate=False
    )
    
    db.session.add_all([production1, production2])
    db.session.commit()
