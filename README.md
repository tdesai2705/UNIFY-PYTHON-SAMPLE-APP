# UNIFY-PYTHON-SAMPLE-APP

A sample Python Flask application with CI/CD pipeline for CloudBees Unify.

## Features

- Simple REST API built with Flask
- Health check endpoint
- Greeting API with parameters
- Unit tests with pytest
- Code coverage reporting
- Linting with flake8
- Automated CI/CD pipeline via CloudBees Unify

## API Endpoints

- `GET /` - Home endpoint
- `GET /health` - Health check
- `GET /api/greet/<name>` - Personalized greeting

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
   - Sets up Python environment
   - Installs dependencies
   - Runs linting
   - Runs tests with coverage
   - Builds the package

2. **Deploy Job:**
   - Runs only on main branch after successful tests
   - Includes deployment placeholder (customize for your needs)

## Deployment

The pipeline automatically deploys to production when code is pushed to the `main` branch.

Customize the deployment step in `.cloudbees/workflows/ci-cd-pipeline.yaml` for your specific deployment target.

## License

MIT

---
*Updated: 2026-03-17*
