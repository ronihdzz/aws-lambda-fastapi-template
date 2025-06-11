# AWS Lambda FastAPI Template

[![English](https://img.shields.io/badge/🇺🇸-English-blue)](README.md) [![Español](https://img.shields.io/badge/🇪🇸-Español-red)](README.es.md)

| Environment | Coverage |
|-----------|----------|
| main | ![Coverage Badge](https://github.com/ronihdzz/aws-lambda-fastapi/blob/artifacts/main/latest/coverage.svg) |
| development | ![Coverage Badge](https://github.com/ronihdzz/aws-lambda-fastapi/blob/artifacts/development/latest/coverage.svg) |

## 📋 Template Description

This is a complete template for developing REST APIs with **FastAPI** designed to be deployed on **AWS Lambda** using **Mangum** as a reverse proxy. The template implements a complete **serverless** approach, providing modular architecture, standardized error handling, automated testing against real databases, and a comprehensive CI/CD stack with Docker.

### 🚀 **Serverless & AWS Lambda Context**

The template is optimized for **serverless architectures** using AWS Lambda:
- **Mangum** acts as an adapter/reverse proxy that allows FastAPI to function as a Lambda function
- **Serverless Computing**: No server management, automatic scaling, pay-per-use
- **API Gateway Integration**: Compatible with AWS API Gateway for routing and authentication
- **Cold Start Optimization**: Structure optimized to minimize cold start time

## 🏗️ Architecture and Project Structure

### Directory Structure

```
aws-lambda-fastapi/
├── src/                          # Main source code
│   ├── api/                      # API layer - Routers and endpoints
│   │   ├── v1/                   # API versioning
│   │   ├── routers.py            # Main router registration
│   │   └── endpoints.py          # Base endpoints (health check, etc.)
│   ├── core/                     # Central configuration
│   │   ├── settings/             # Environment-specific configurations
│   │   ├── exceptions.py         # Domain-specific exceptions
│   │   └── internal_codes.py     # Domain internal codes
│   ├── shared/                   # Shared utilities
│   │   ├── middlewares/          # Custom middlewares
│   │   ├── base_responses.py     # Standardized responses
│   │   ├── base_internal_codes.py # Base internal codes
│   │   ├── base_exceptions.py    # Base exceptions
│   │   └── utils_dates.py        # Date utilities
│   ├── db/                       # Database layer
│   │   ├── postgresql/           # PostgreSQL configuration
│   │   └── mongo/                # MongoDB configuration
│   ├── tests/                    # Test suite
│   └── main.py                   # Application entry point
├── docker_images/                # Custom Docker images
│   └── testing/                  # Testing configuration
├── .github/workflows/            # CI/CD pipelines
└── docs/                         # Project documentation
```

## 🔧 Main Components

### 1. **Standardized Response System** (`@/shared/base_responses.py`)

This template implements a consistent response system using an **Envelope Response** pattern:

```python
class EnvelopeResponse(BaseModel):
    success: bool
    message: str
    data: dict[str, Any] | list | None = None
    trace_id: str | None = None
```

**Conventions:**
- All responses follow the same format
- Automatic Pydantic model serialization handling
- Trace_id inclusion for debugging
- Structured error responses with internal codes

### 2. **Internal Code System** (`@/shared/base_internal_codes.py`)

Standardized error code system for tracking and debugging:

```python
class CommonInternalCode(InternalCodeBase):
    UNKNOWN = 100, "Unknown error"
    PYDANTIC_VALIDATIONS_REQUEST = 8001, "Failed Pydantic validations on request"
```

**Conventions:**
- Unique numeric codes for each error type
- Clear error description
- Extensible for domain-specific codes in `@/core/internal_codes.py`

### 3. **Error Handling Middleware** (`@/shared/middlewares/`)

#### CatcherExceptions
Main middleware that catches all exceptions:
- FastAPI HTTPException handling
- SQLAlchemy NoResultFound handling
- Custom exception handling
- Automatic conversion to standardized response format

#### CatcherExceptionsPydantic
Specific middleware for Pydantic validation errors:
- Catches request body validation errors
- Consistent validation error formatting

### 4. **Configuration System** (`@/core/settings/`)

Environment-based configuration using Pydantic Settings:

```
settings/
├── base.py           # Base configuration
├── local.py          # Local development
├── development.py    # Development environment
├── staging.py        # Staging environment
├── production.py     # Production environment
└── testing.py        # Testing configuration
```

**Conventions:**
- Typed environment variables
- Automatic configuration validation
- Environment-specific configuration
- Multi-database support

### 5. **Multi-Database System** (`@/db/`)

Template prepared for multiple database managers with **functional examples**:

#### PostgreSQL (`@/db/postgresql/`)
```
postgresql/
├── base.py           # Base class for SQLAlchemy models
├── connection.py     # Connection configuration
├── models/
│   └── public/       # 'public' schema
│       └── book.py   # Example model
└── __init__.py       # Main exports
```

- **SQLAlchemy 2.0**: Modern ORM with modern syntax
- **Typed Models**: Full type hints and validation
- **Singleton Connection**: Reusable and efficient

#### MongoDB (`@/db/mongo/`)
```
mongo/
├── base.py           # Base class for documents
├── connection.py     # Configured MongoDB client
├── models/           # Document models
└── __init__.py       # Main exports
```

- **PyMongo**: Official MongoDB driver
- **Pydantic Integration**: Models with automatic validation
- **Async Ready**: Prepared for asynchronous operations

**Conventions:**
- Models organized by schemas/collections
- Singleton connection pattern
- Environment-specific configuration
- **Extensible**: Easy to add Redis, DynamoDB, etc.

### 6. **Modular API Structure** (`@/api/`)

Versioning system and modular organization by domain:

```
api/
├── v1/                    # API Version 1
│   └── books/             # Domain module (example)
│       ├── endpoints.py   # Defines REST endpoints
│       ├── repositories.py # Database access
│       ├── schema.py      # Pydantic models (DTOs)
│       └── services.py    # Business logic
├── routers.py             # Global router registration
└── endpoints.py           # Base endpoints (health, index)
```

**Module Conventions:**
- **endpoints.py**: Route definition and input validations
- **services.py**: Business logic, orchestration
- **repositories.py**: Data access, specific queries
- **schema.py**: DTOs (Data Transfer Objects) with Pydantic

**Scalability**: You can add more modules (`users/`, `orders/`, etc.) following the same structure.

### 7. **Testing System** (`@/tests/`)

Complete automated testing suite:

```
tests/
├── common/           # Common utilities for tests
├── utils/            # Testing utilities
├── v1/               # Version-specific tests
└── __init__.py       # Database configuration for tests
```

**Conventions:**
- **Separate testing database**: Automatic configuration via `environment_testing`
- **Reusable fixtures**: Common utilities in `tests/common/`
- **Automated coverage**: Integrated in CI/CD with detailed reports
- **Tests organized by version**: Modular structure by API version
- **Automatic setup**: The `prepare_database()` script creates necessary schemas and tables each time the runner starts

### 8. **Comprehensive Docker Stack** (`@/docker_images/`)

The project comprehensively organizes Docker images for different purposes:

#### **Testing Docker** (`@/docker_images/testing/`)
Specialized configuration for testing against **real databases** (not mocks):

- **`Dockerfile.testing`**: Optimized image for running tests
- **`ci.env.sh`**: Script that configures environment variables for CI/CD
- **`entrypoint.sh`**: Orchestrates test execution and report generation

**Database Selection in CI:**
```bash
# In ci.env.sh you can select which databases to spin up
export POSTGRESQL_URL="${GITHUB_DATABASE_POSTGRESQL:-$POSTGRESQL_URL}"
export MONGO_URL="${GITHUB_DATABASE_MONGODB:-$MONGO_URL}"
export REDIS_URL="${GITHUB_DATABASE_REDIS:-$REDIS_URL}"
```

Tests run against **real instances** of PostgreSQL, MongoDB, and Redis in the GitHub Actions runner.

#### **Build and Deploy Docker**
- **`docker_images/build/`**: Optimized construction image
- **`docker_images/deploy/`**: Final image for AWS Lambda deployment

## 🚀 Complete CI/CD Pipelines

### **Main GitHub Actions Flow**

The pipeline executes a complete and robust sequence:

#### **1. 🔍 Linting (Pre-commit)**
```yaml
- Executes pre-commit for linting (configured in .pre-commit-config.yaml)
- Code formatting with Black
- Linting with Flake8  
- Type checking with MyPy
- Import and structure validation
```

#### **2. 🧪 Testing with Real Databases**
```yaml
services:
  postgres: # PostgreSQL 13 on port 5432
  mongodb:  # MongoDB 4.4 on port 27017  
  redis:    # Redis 6 on port 6379
```
- Spins up real database services
- Runs tests against real instances (not mocks)
- Generates detailed coverage reports

#### **3. 📊 Coverage and Badges**
- **Generation**: `coverage run`, `coverage xml`, `coverage-badge`
- **Archival**: Uses `ronihdzz/git-archive-action@v3` to save artifacts
- **Storage**: Reports are stored in dedicated `artifacts` branch
- **Badges**: Dynamic coverage % badges are generated and displayed in README

#### **4. 🏗️ Build and Deploy**
- Docker image construction optimized for Lambda
- Push to Amazon ECR (Elastic Container Registry)
- Automatic deploy to AWS Lambda
- Automatic versioning by environment (dev/staging/prod)

### **Environment Configuration**

```yaml
BRANCH_ENV_MAP: 
  "main": "prod"
  "development": "dev" 
  "staging": "stg"
```

Each branch automatically maps to its corresponding environment.

## 📦 Dependencies and Technologies

### Core Dependencies
- **FastAPI**: Modern and fast web framework
- **Mangum**: Adapter for AWS Lambda
- **Pydantic**: Data validation and settings
- **SQLAlchemy**: ORM for relational databases
- **PyMongo**: MongoDB driver
- **Loguru**: Advanced logging

### Development Dependencies
- **Pytest**: Testing framework
- **Coverage**: Code coverage
- **MyPy**: Type checking
- **Pre-commit**: Pre-commit hooks

## 🛠️ Development Commands

### Run the project locally
```bash
uvicorn main:app --reload --port=9595
```

### Run tests
```bash
pytest src/tests/ -v --cov=src
```

### Run pre-commit hooks
```bash
pre-commit run --all-files
```

### Type checking
```bash
mypy src/
```

### Testing with Docker
```bash
docker-compose -f docker-compose.yml up testing
```

## 🔍 Lambda Local Testing

To test the Lambda function locally:

```bash
curl -X POST "http://localhost:9100/2015-03-31/functions/function/invocations" \
  -H "Content-Type: application/json" \
  -d '{
    "version": "2.0",
    "routeKey": "GET /",
    "rawPath": "/",
    "rawQueryString": "",
    "headers": {},
    "requestContext": {
      "http": {
        "method": "GET",
        "path": "/",
        "sourceIp": "127.0.0.1"
      }
    },
    "isBase64Encoded": false
  }'
```

## 🎯 **Template Advantages**

### **For Development**
- **Serverless Ready**: Optimized for AWS Lambda with Mangum
- **Multi-Database**: Native support for PostgreSQL, MongoDB, Redis
- **Type Safety**: Full TypeScript-like experience with MyPy
- **Error Handling**: Robust error handling system with internal codes

### **For Testing**
- **Real Databases**: Tests against real databases, not mocks
- **Automated Setup**: Automatic creation of schemas and test data
- **Coverage Tracking**: Detailed reports with automatic badges
- **Docker Isolated**: Completely isolated testing environment

### **For CI/CD**
- **Full Pipeline**: Linting → Testing → Coverage → Build → Deploy
- **Multi-Environment**: Automatic support for dev/staging/prod
- **Quality Gates**: Pre-commit hooks and automatic validations
- **Artifact Management**: Automatic storage of reports and badges

### **For Production**
- **AWS Optimized**: Configured for AWS Lambda + API Gateway
- **Environment Config**: Typed configuration per environment
- **Monitoring Ready**: Structured logging with Loguru + Sentry
- **Scalable Architecture**: Modular structure easy to scale
