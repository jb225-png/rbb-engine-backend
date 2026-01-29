# RBB Engine Backend

AI-powered educational content generation backend built with FastAPI and Claude AI integration.

## Overview

The RBB Engine Backend is a comprehensive system for generating educational content including worksheets, quizzes, passages, and assessments. It features AI-driven content generation, quality control, and metadata creation with support for multiple curricula (CBSE, Common Core) and locales.

## Key Features

- **AI Content Generation**: Claude Sonnet 4 integration for educational content creation
- **Quality Control**: Automated QC scoring and validation system
- **Metadata Generation**: SEO-optimized titles, descriptions, and pricing suggestions
- **Multi-Curriculum Support**: CBSE (India) and Common Core (US) standards
- **RESTful API**: Comprehensive API with automatic documentation
- **Database Management**: PostgreSQL with Alembic migrations
- **File Storage**: Organized storage system for generated content

## Tech Stack

- **FastAPI** - Modern Python web framework
- **SQLAlchemy** - Database ORM with declarative models
- **PostgreSQL** - Primary database
- **Alembic** - Database migration management
- **Pydantic v2** - Data validation and serialization
- **Claude AI** - Content generation via Anthropic's API
- **ReportLab** - PDF generation
- **Uvicorn** - ASGI server

## Project Structure

```
rbb-engine-backend/
├── app/
│   ├── ai/                     # AI agents and processing
│   │   ├── agents/            # Generator, QC, and Metadata agents
│   │   ├── prompts/           # AI prompt templates
│   │   ├── schemas/           # AI response validation schemas
│   │   └── claude_client.py   # Claude API integration
│   ├── api/v1/routes/         # API endpoints
│   ├── core/                  # Configuration and settings
│   ├── db/                    # Database session management
│   ├── models/                # SQLAlchemy database models
│   ├── schemas/               # Pydantic request/response schemas
│   ├── repositories/          # Data access layer
│   ├── services/              # Business logic
│   ├── utils/                 # Utilities and helpers
│   └── main.py               # FastAPI application factory
├── migrations/               # Alembic database migrations
├── rbb-drive/               # Generated content storage
├── scripts/                 # Utility scripts
├── requirements.txt         # Python dependencies
├── alembic.ini             # Alembic configuration
├── run.py                  # Development server runner
└── .env.example           # Environment variables template
```

## Quick Start

### 1. Environment Setup

```bash
# Create and activate virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Edit .env with your configuration
```

### 2. Database Setup

```bash
# Create PostgreSQL database
createdb rbb_engine

# Run migrations
alembic upgrade head

# Seed standards (optional)
python scripts/seed_standards.py
```

### 3. Start Development Server

```bash
# Using uvicorn directly
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Or using the runner script
python run.py
```

The API will be available at:
- **API**: http://localhost:8000
- **Documentation**: http://localhost:8000/docs
- **Alternative Docs**: http://localhost:8000/redoc

## Environment Variables

Create a `.env` file with the following variables:

```env
# Database
DATABASE_URL=postgresql://username:password@localhost/rbb_engine

# Claude AI
CLAUDE_API_KEY=your-claude-api-key-here
CLAUDE_MODEL=claude-3-5-sonnet-20241022
CLAUDE_TIMEOUT=60
CLAUDE_MAX_RETRIES=3

# Application
APP_NAME=RBB Engine Backend
DEBUG=true
LOG_LEVEL=info

# Storage
STORAGE_PATH=./rbb-drive
```

## Core API Endpoints

### Content Generation
- `POST /api/generate-product` - Generate educational content
- `GET /api/products` - List generated products
- `GET /api/products/{id}` - Get specific product
- `GET /api/products/{id}/download/pdf` - Download product as PDF

### Standards Management
- `GET /api/v1/standards` - List educational standards
- `GET /api/v1/standards/{id}` - Get specific standard
- `POST /api/v1/standards` - Create new standard

### Generation Jobs
- `GET /api/v1/generation-jobs` - List generation jobs
- `GET /api/v1/generation-jobs/{id}` - Get job details
- `POST /api/v1/generation-jobs` - Create generation job

### Dashboard & Analytics
- `GET /api/dashboard/stats` - Dashboard statistics
- `GET /api/dashboard/summary` - Dashboard summary

### System
- `GET /api/health` - Health check with database connectivity

## AI Content Generation

The system uses a modular AI agent architecture:

### Generator Agent
- Creates educational content based on curriculum standards
- Supports multiple product types (worksheets, quizzes, passages, assessments)
- Validates output against strict JSON schemas

### QC Agent
- Evaluates content across 6 dimensions (structure, alignment, clarity, difficulty, inclusivity, accuracy)
- Provides scores and verdicts (PASS/NEEDS_FIX/FAIL)
- Generates detailed feedback and recommendations

### Metadata Agent
- Creates SEO-optimized titles and descriptions
- Suggests appropriate pricing based on content complexity
- Generates relevant tags and keywords

## Database Models

### Core Entities
- **Standards** - Educational standards (CBSE, Common Core)
- **Products** - Generated educational content
- **Generation Jobs** - Content generation tasks with progress tracking
- **Upload Tasks** - VA team workflow management
- **File Artifacts** - Generated files and metadata

### Status Lifecycles
- **Products**: DRAFT → GENERATED (success) / FAILED (error)
- **Jobs**: PENDING → RUNNING → COMPLETED (success) / FAILED (error)

## Development

### Running Tests
```bash
# Run all tests
python -m pytest

# Run with coverage
python -m pytest --cov=app tests/
```

### Database Migrations
```bash
# Create new migration
alembic revision --autogenerate -m "Description of changes"

# Apply migrations
alembic upgrade head

# Rollback migration
alembic downgrade -1
```

### Code Quality
```bash
# Format code
black app/

# Lint code
flake8 app/

# Type checking
mypy app/
```

## Production Deployment

### Docker Deployment
```bash
# Build image
docker build -t rbb-engine-backend .

# Run container
docker run -p 8000:8000 --env-file .env rbb-engine-backend
```

### Environment Configuration
- Set `DEBUG=false` for production
- Use proper PostgreSQL connection string
- Configure Claude API key
- Set up proper logging levels
- Configure CORS origins appropriately

## API Documentation

The API is fully documented with OpenAPI/Swagger:
- Interactive documentation at `/docs`
- OpenAPI JSON schema at `/openapi.json`
- Alternative documentation at `/redoc`

## Monitoring & Logging

- Structured logging with configurable levels
- Health check endpoint for monitoring
- Database connectivity verification
- Error tracking and reporting

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Ensure all tests pass
6. Submit a pull request

## License

This project is proprietary software. All rights reserved.