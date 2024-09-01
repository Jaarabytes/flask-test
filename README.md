# Flask Transaction API

This is a Flask-based API that accepts transaction data, processes it, and securely stores it in a PostgreSQL database. The API provides a simple and efficient way to handle transactions in your application.

## Features

- RESTful API endpoints for submitting transaction data
- Secure and efficient storage of transaction data in a PostgreSQL database 
- Easy integration with other applications and services

## Requirements

- Python 3.x
- Pip

### Installation

- Clone the repository:


```
https://github.com/Jaarabytes/flask-test.git
```

- Navigate into the project directory:


```
cd flask-test
```		

- Create a virtual environment (optional but recommended):


```
python -m venv venv
```		

- Activate the virtual environment:

    - Windows:

```
        venv\Scripts\activate
```

    - Linux/Mac OS:

```
        source venv/bin/activate
```

- Install the required packages:


```
pip install -r requirements.txt
```		

- Set up the environment variables:
    - Copy the contents of .env.example into a new file named .env
    - Update the values in the .env file with your PostgreSQL credentials and other configuration details
    - Make sure that the credentials start with the format `postgresql+pg8000://`

### Usage

Start the Flask development server:
```
python app.py
```	

The API will be available at http://localhost:5000 (or another port if you've configured it differently)

Use a tool like Postman or curl to send HTTP requests to the API endpoints

## Tests

Tests are already written. 

To run the tests:

```
pytest tests.py
```

## Contributing

- Fork the repository
- Create your feature branch (git checkout -b feature/new-feature)
- Commit your changes (git commit -am 'Add new feature')
- Push to the branch (git push origin feature/new-feature)
- Create a new Pull Request

## License

This project is licensed under the MIT License.
