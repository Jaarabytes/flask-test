# All tests involving the Flask API are implemented here
# The test function names are pretty descriptive thus no need for comments

import pytest
from app import create_app, Base, Transaction
from sqlalchemy.orm import sessionmaker
import os
import os
import pytest
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

load_dotenv()
# ======================================================
# Seting up the test environment
# ======================================================
@pytest.fixture(scope='module')
def test_app():
    app = create_app()
    with app.app_context():
        yield app

@pytest.fixture(scope='module')
def test_client(test_app):
    return test_app.test_client()

# ======================================================
# Sets up and tears down the database and app
# ======================================================

@pytest.fixture(scope='module')
async def init_database():
    database_uri = os.getenv("DB_URI")
    async_engine = create_async_engine(database_uri, echo=True)

    # Create all tables asynchronously
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    # Set up the session maker
    AsyncSessionLocal = sessionmaker(bind=async_engine,class_=AsyncSession,expire_on_commit=False)

    async with AsyncSessionLocal() as session:
        yield session

        # Clean up the test data asynchronously
        await session.execute("DELETE FROM transactions")
        await session.commit()

# ======================================================
# Test cases start here
# ======================================================
def test_submit_endpoint(test_client, init_database):
    response = test_client.post('/submit', json={
        "transaction_id": "12345",
        "user_id": "67890",
        "amount": 100.0,
        "currency": "USD",
        "timestamp": "2024-08-31T12:34:56"
    })

    assert response.status_code == 201
    assert response.json == {"message": "Transaction stored successfully!"}

def test_submit_endpoint_missing_field(test_client):
    response = test_client.post('/submit', json={
        "transaction_id": "12345",
        "user_id": "67890",
        "amount": 100.0,
        # Missing currency and timestamp fields
    })

    assert response.status_code == 500

def test_submit_endpoint_invalid_data_type(test_client):
    # amount should be an integer, not a string
    response = test_client.post('/submit', json={
        "transaction_id": "12345",
        "user_id": "67890",
        "amount": "150",
        "currency": "USD",
        "timestamp": "2024-08-31T12:34:56"
    })

    assert response.status_code == 400
    assert response.json == {"error": "Amount must be a positive number"}

def test_submit_endpoint_negative_amount(test_client):
    response = test_client.post('/submit', json={
        "transaction_id": "12345",
        "user_id": "67890",
        "amount": -50.0,
        "currency": "USD",
        "timestamp": "2024-08-31T12:34:56"
    })

    assert response.status_code == 400
    assert response.json == {"error": "Amount must be a positive number"}

def test_submit_endpoint_zero_amount(test_client):
    # Test a POST request with an invalid amount, zero dollars
    response = test_client.post('/submit', json={
        "transaction_id": "12345",
        "user_id": "67890",
        "amount": 0,
        "currency": "USD",
        "timestamp": "2024-08-31T12:34:56"
    })

    assert response.status_code == 400
    assert response.json == {"error": "Amount must be a positive number"}
