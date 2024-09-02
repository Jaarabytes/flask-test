import os
from flask import Flask
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
import asyncio
from flask import Flask, request, jsonify
from dotenv import load_dotenv
from sqlalchemy import Column, String, Float, DateTime
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError
from datetime import datetime
from celery.result import AsyncResult
from celery_tasks import make_celery
import requests
import asyncpg
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import asyncio


load_dotenv()

Base = declarative_base()
app = Flask(__name__)

# Configure Flask app for Celery
app.config['CELERY_BROKER_URL'] = 'redis://localhost:6379/0'
app.config['CELERY_RESULT_BACKEND'] = 'redis://localhost:6379/0'

# Initialize Celery
celery = make_celery(app)

database_uri = os.getenv("DB_URI")
celery.conf.update(app.config)
async_engine = create_async_engine(database_uri,pool_size=20,max_overflow=30)
AsyncSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=async_engine, class_=AsyncSession)

class Transaction(Base):
    __tablename__ = "transactions"

    transaction_id = Column(String, primary_key=True, index=True)
    user_id = Column(String, index=True)
    amount = Column(Float)
    currency = Column(String)
    timestamp = Column(DateTime)

class Processed_Transactions(Base):
    __tablename__ = "processed_transactions"

    transaction_id = Column(String, primary_key=True, index=True)
    user_id = Column(String, index=True)
    amount = Column(Float)
    currency = Column(String)
    timestamp = Column(DateTime)

# Function to create tables asynchronously
async def create_tables():
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

def create_app(config_name='default'):
    app = Flask(__name__)
    asyncio.run(create_tables())
    def get_db():
        db = AsyncSessionLocal()
        try:
            yield db
        finally:
            db.close()

    @app.route('/submit', methods=['POST'])
    def submit():
        data = request.get_json()
        # Start the Celery task
        task = process_transaction.delay(
            data['transaction_id'],
            data['user_id'],
            data['amount'],
            data['currency'],
            data['timestamp']
        )
        print(f"Task added: {jsonify({'task_id': task.id})}")
        try:
            transaction_id = data['transaction_id']
            user_id = data['user_id']
            amount = data['amount']
            currency = data['currency']
            timestamp = datetime.fromisoformat(data['timestamp'])
        except KeyError as e:
            return jsonify({"error": f"Missing field: {str(e)}"}), 400
        except ValueError:
            return jsonify({"error": "Invalid timestamp format"}), 400
        
        if not isinstance(amount, (int, float)) or amount <= 0:
            return jsonify({"error": "Amount must be a positive number"}), 400

        transaction = Transaction(
            transaction_id=transaction_id,
            user_id=user_id,
            amount=amount,
            currency=currency,
            timestamp=timestamp
        )

        db = next(get_db())
        try:
            db.add(transaction)
            db.commit()
        except SQLAlchemyError as e:
            db.rollback()
            app.logger.error(f"Database error: {str(e)}")
            return jsonify({"error": "Failed to store data"}), 500
        finally:
            db.close()
        
        return jsonify({"message": "Transaction stored successfully!"}), 201
        
    @celery.task(bind=True)
    async def process_transaction(self, transaction_id, user_id, amount, currency, timestamp):
        converted_amount = convert_currency(amount)

        # Connect to the database using asyncpg
        conn = await asyncpg.connect(os.getenv('DATABASE_URI'))
        
        # Insert the data into the database
        await conn.execute(
            "INSERT INTO processed_transactions (transaction_id, user_id, amount, currency, timestamp) VALUES ($1, $2, $3, $4, $5)",
            transaction_id, user_id, converted_amount, currency, timestamp
        )
        
        await conn.close()

        return {"status": "Transaction processed", "transaction_id": transaction_id}

    def convert_currency(amount):
        api_key = os.getenv("RATES_API")
        url = f'https://api.currencybeacon.com/v1/latest?api_key={api_key}&base=USD'
        response = requests.get(url)
        
        if response.status_code == 200:
            data = response.json()
            rate = data['response']['rates']['EUR']
            return int(rate) * amount 
        else:
            return None

    @app.route('/task_status/<task_id>', methods=['GET'])
    def task_status(task_id):
        task = AsyncResult(task_id)
        
        if task.state == 'PENDING':
            response = {
                'state': task.state,
                'status': 'Pending...'
            }
        elif task.state == 'FAILURE':
            response = {
                'state': task.state,
                'status': str(task.info)
            }
        else:
            response = {
                'state': task.state,
                'status': task.info.get('status', ''),
                'result': task.info.get('result', '')
            }
        
        return jsonify(response)
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=False)
