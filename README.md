# FastAPI Secure Users

## Overview

This project demonstrates a secure user management API built with FastAPI, SQLAlchemy, and Pydantic. It implements secure password hashing, input validation, PostgreSQL database integration, automated testing, containerization with Docker, and a complete CI/CD pipeline using GitHub Actions.

## Features

- Secure SQLAlchemy User model
- Password hashing and verification
- Pydantic request and response validation
- PostgreSQL database integration
- Unit, integration, and end-to-end tests
- Docker containerization
- GitHub Actions CI/CD pipeline
- Trivy security vulnerability scanning
- Automatic Docker Hub deployment

---

## Running the Application

Clone the repository:

```bash
git clone https://github.com/Benkaii/fastapi_secure_users.git
cd fastapi_secure_users
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Start the application:

```bash
uvicorn main:app --reload
```

The API will be available at:

```
http://127.0.0.1:8000
```

Swagger documentation:

```
http://127.0.0.1:8000/docs
```

---

## Running Tests Locally

Run all tests:

```bash
pytest
```

Run only unit tests:

```bash
pytest tests/unit -v
```

Run only integration tests:

```bash
pytest tests/integration -v
```

Run only end-to-end tests:

```bash
pytest tests/e2e -v
```

Run tests with coverage:

```bash
pytest --cov=app --cov-report=term-missing
```

---

## Docker

Build the Docker image:

```bash
docker build -t fastapi_secure_users .
```

Run the Docker container:

```bash
docker run -p 8000:8000 fastapi_secure_users
```

---

## Docker Hub Repository

Docker Image:

https://hub.docker.com/r/benkaii/fastapi_secure_users

Pull the latest image:

```bash
docker pull benkaii/fastapi_secure_users:latest
```

---

## GitHub Repository

https://github.com/Benkaii/fastapi_secure_users

---

## CI/CD Pipeline

GitHub Actions automatically performs the following:

- Runs unit tests
- Runs integration tests with PostgreSQL
- Runs end-to-end tests
- Performs Trivy security scanning
- Builds the Docker image
- Pushes the Docker image to Docker Hub after successful validation

---

## Technologies Used

- Python 3.10
- FastAPI
- SQLAlchemy
- PostgreSQL
- Pydantic
- Pytest
- Playwright
- Docker
- GitHub Actions
- Trivy