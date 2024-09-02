# Flask Transaction API

This is a Flask-based API that accepts transaction data, processes it, and securely stores it in a PostgreSQL database. The API provides a simple and efficient way to handle transactions in your application.

## Features

- RESTful API endpoints for submitting transaction data
- Secure and efficient storage of transaction data in a PostgreSQL database 
- Easy integration with other applications and services

## Requirements

- Python 3.x
- Poetry
- RabittMQ
- Redis

### Installation

- Clone the repository:


```
https://github.com/Jaarabytes/flask-test.git
```

- Navigate into the project directory:


```
cd flask-test
```		

- Activate the virtual environment:

    - Windows:

```
poetry shell
```

    - Linux/Mac OS:

```
poetry shell
```

- Install the required packages:


```
poetry install
```		

- Set up the environment variables:
    - Copy the contents of .env.example into a new file named .env
    - Update the values in the .env file with your PostgreSQL credentials and other configuration details
    - Make sure that the credentials start with the format `postgresql+asyncpg://`

### Usage

Start the Flask development server:
```
python app/app.py
```	

Start the celery and redis workers:

```
celery -A celery worker --loglevel=info
sudo systemctl start redis && sudo systemctl enable redis
```

Testing the load using locust:

```
locust -f tests/locustfile.py
```

Proceed to the web interface and tinker the settings to your liking

## Tests

Tests are already written. 

To run the tests:

```
pytest tests/tests.py
```

## Contributing

- Fork the repository
- Create your feature branch (git checkout -b feature/new-feature)
- Commit your changes (git commit -am 'Add new feature')
- Push to the branch (git push origin feature/new-feature)
- Create a new Pull Request

## License

This project is licensed under the MIT License.
