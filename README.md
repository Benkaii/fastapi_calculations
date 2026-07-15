# FastAPI Calculation Model

## Overview

This project builds on the secure FastAPI user application from Module 10 by adding a SQLAlchemy Calculation model, Pydantic validation, calculation factory logic, PostgreSQL integration tests, and automated Docker deployment.

The Calculation model supports addition, subtraction, multiplication, and division. Calculations are associated with valid users through a foreign-key relationship.

## Features

- SQLAlchemy User and Calculation models
- Calculation fields for `a`, `b`, `type`, `result`, and `user_id`
- Foreign-key relationship between calculations and users
- Pydantic `CalculationCreate` and `CalculationRead` schemas
- Validation for supported calculation types
- Division-by-zero validation
- Factory pattern for calculation operations
- Unit and PostgreSQL integration tests
- Docker containerization
- GitHub Actions CI/CD pipeline
- Trivy container security scanning
- Automatic Docker Hub deployment

## Clone the Repository

```bash
git clone https://github.com/Benkaii/fastapi_calculations.git
cd fastapi_calculations
```

## Install Dependencies

```bash
pip install -r requirements.txt
```

## Run with Docker Compose

```bash
docker compose up -d --build
```

The FastAPI application will be available at:

```text
http://localhost:8000
```

Swagger documentation:

```text
http://localhost:8000/docs
```

## Run Tests Locally

Run unit and integration tests inside Docker:

```bash
docker compose exec web pytest tests/unit tests/integration -v
```

Run unit tests only:

```bash
pytest tests/unit -v
```

Run integration tests only:

```bash
pytest tests/integration -v
```

Run tests with coverage:

```bash
pytest tests/unit tests/integration --cov=app --cov-report=term-missing
```

## Docker Hub

Docker Hub repository:

```text
https://hub.docker.com/r/benkaii/fastapi_calculations
```

Pull the latest image:

```bash
docker pull benkaii/fastapi_calculations:latest
```

## GitHub Repository

```text
https://github.com/Benkaii/fastapi_calculations
```

## CI/CD Pipeline

GitHub Actions automatically:

- Starts a PostgreSQL service
- Runs unit and integration tests
- Enforces test coverage
- Builds the Docker image
- Scans the image with Trivy
- Pushes the image to Docker Hub after successful testing and scanning

## Technologies Used

- Python 3.10
- FastAPI
- SQLAlchemy
- PostgreSQL
- Pydantic
- Pytest
- Docker
- GitHub Actions
- Trivy