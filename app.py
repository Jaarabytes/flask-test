import os
from flask import Flask, request, jsonify
from dotenv import load_dotenv
from sqlalchemy import create_engine, Column, String, Float, DateTime
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.pool import QueuePool
from sqlalchemy.exc import SQLAlchemyError
from datetime import datetime

load_dotenv()

app = Flask(__name__)

database_uri = os.getenv("DB_URI")
engine = create_engine(database_uri, poolclass=QueuePool, pool_size=20, max_overflow=30)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

class Transaction(Base):
    __tablename__ = "transactions"

    transaction_id = Column(String, primary_key=True, index=True)
    user_id = Column(String, index=True)
    amount = Column(Float)
    currency = Column(String)
    timestamp = Column(DateTime)

Base.metadata.create_all(bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.route('/submit', methods=['POST'])
def submit():
    data = request.get_json()

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
    # Prevent negative or zero amount transactions    
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

if __name__ == '__main__':
    app.run(debug=False)
