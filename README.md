# UNIFY-PYTHON-SAMPLE-APP

A sample Python Flask application with CI/CD pipeline for CloudBees Unify.

## Features

- RESTful API built with Flask
- Full CRUD operations for items
- Swagger/OpenAPI documentation
- Health check endpoint
- Greeting API with parameters
- Unit tests with pytest (98% coverage)
- Code coverage reporting with threshold enforcement
- Linting with flake8
- Automated CI/CD pipeline via CloudBees Unify
- Docker support

## API Documentation

Interactive API documentation is available via Swagger UI:

**Local:** http://localhost:5000/api/docs

The Swagger UI provides:
- Complete API reference
- Try-it-out functionality for all endpoints
- Request/response schemas
- Example payloads

## API Endpoints

### General
- `GET /` - Home endpoint with API information
- `GET /health` - Health check
- `GET /api/greet/<name>` - Personalized greeting
- `GET /api/docs` - Swagger UI documentation

### Items CRUD
- `GET /api/items` - Get all items
- `GET /api/items/<id>` - Get item by ID
- `POST /api/items` - Create new item
- `PUT /api/items/<id>` - Update item
- `DELETE /api/items/<id>` - Delete item

## Local Development

### Prerequisites

- Python 3.9+
- pip

### Installation

```bash
# Install dependencies
pip install -r requirements.txt
```

### Running the Application

```bash
python app.py
```

The application will start on `http://localhost:5000`

### Running Tests

```bash
# Run tests
pytest

# Run tests with coverage
pytest --cov=. --cov-report=term
```

### Linting

```bash
flake8 . --count --select=E9,F63,F7,F82 --show-source --statistics
```

## CI/CD Pipeline

The project includes a CloudBees Unify pipeline configuration in `.cloudbees/workflows/ci-cd-pipeline.yaml` that:

1. **Build & Test Job:**
   - Checks out code
   - Runs linting with flake8
   - Runs tests with pytest (18 tests, 98% coverage)
   - Enforces 80% coverage threshold
   - Builds Python package
   - Validates Dockerfile for Docker Hub publishing

2. **Deploy Jobs:**
   - **Staging:** Deploys to staging environment (develop branch)
   - **Production:** Deploys to production environment (main branch)

### Docker Hub Publishing

The pipeline is configured to publish Docker images to Docker Hub:

**Image Repository:** `tdesai2705/unify-python-app`

**Tags:**
- `latest` - Most recent build
- `<commit-sha>` - Specific version

**Setup Required:** See [DOCKER_HUB_SETUP.md](DOCKER_HUB_SETUP.md) for configuration instructions

## Deployment

The pipeline automatically deploys to production when code is pushed to the `main` branch.

Customize the deployment step in `.cloudbees/workflows/ci-cd-pipeline.yaml` for your specific deployment target.

## License

MIT

---
*Updated: 2026-03-17*
