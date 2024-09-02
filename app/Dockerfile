FROM python:3.11-slim

WORKDIR /app

RUN curl -sSL https://install.python-poetry.org | python3 -

COPY . /app

RUN poetry shell
RUN poetry install

# Make port 5000 available to the world outside this container
EXPOSE 5000

# Define environment variables
ENV FLASK_APP=app.py

# Run the application
CMD ["flask", "run", "--host=0.0.0.0"]
