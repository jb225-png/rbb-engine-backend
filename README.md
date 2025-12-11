# RBB Engine Backend

AI-powered curriculum generation backend built with FastAPI.

## Project Structure

```
rbb-engine-backend/
├── app/
│   ├── api/v1/routes/
│   │   ├── health.py              # Health check endpoint
│   │   ├── standards.py           # Standards management
│   │   ├── products.py            # Product management
│   │   ├── generation_jobs.py     # Job tracking
│   │   ├── upload_tasks.py        # VA team tasks
│   │   └── dashboard.py           # Dashboard endpoints
│   ├── core/
│   │   ├── config.py              # Config exports
│   │   ├── settings.py            # Environment settings
│   │   └── responses.py           # Response helpers
│   ├── db/
│   │   ├── base.py                # Model imports for Alembic
│   │   └── session.py             # Database session management
│   ├── models/
│   │   ├── standard.py            # Standard model
│   │   ├── product.py             # Product model
│   │   ├── generation_job.py      # Generation job model
│   │   ├── upload_task.py         # Upload task model
│   │   ├── file_artifact.py       # File artifact model
│   │   ├── job.py                 # Legacy job model
│   │   └── __init__.py
│   ├── schemas/
│   │   ├── standard.py            # Standard Pydantic schemas
│   │   ├── product.py             # Product Pydantic schemas
│   │   ├── generation_job.py      # Generation job schemas
│   │   ├── upload_task.py         # Upload task schemas
│   │   ├── file_artifact.py       # File artifact schemas
│   │   ├── job.py                 # Legacy job schemas
│   │   └── __init__.py
│   ├── services/
│   │   └── __init__.py            # Business logic (Day 3+)
│   ├── utils/
│   │   ├── logger.py              # Logging configuration
│   │   └── storage.py             # File storage utilities
│   └── main.py                    # FastAPI app factory
├── docs/
│   ├── entities.md                # Database entities documentation
│   └── endpoints_mvp.md           # MVP API endpoints documentation
├── migrations/                     # Alembic migrations
│   ├── env.py
│   └── script.py.mako
├── alembic.ini                    # Alembic configuration
├── requirements.txt               # Python dependencies
├── .env.example                   # Environment template
└── README.md
```

## Setup Instructions

### 1. Activate Virtual Environment

```bash
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure Environment

```bash
cp .env.example .env
# Edit .env with your database credentials
```

### 4. Setup Database

Make sure PostgreSQL is running, then create the database:

```bash
createdb rbb_engine
```

### 5. Run Migrations

```bash
# Generate migration (after activating venv)
alembic revision --autogenerate -m "Add core entities"
# Apply migration
alembic upgrade head
```

### 6. Start Development Server

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

The API will be available at: http://localhost:8000

API documentation: http://localhost:8000/docs

## Available Endpoints

### Core Endpoints
- `GET /api/health` - Health check endpoint
- `GET /api/v1/standards` - List standards
- `GET /api/v1/products` - List products
- `POST /api/v1/generation-jobs` - Create generation job
- `GET /api/v1/upload-tasks` - List upload tasks
- `GET /api/v1/dashboard/stats` - Dashboard statistics

See `docs/endpoints_mvp.md` for complete endpoint documentation.

## Documentation

- **Entity Documentation**: `docs/entities.md` - Database entities and their purpose
- **API Documentation**: `docs/endpoints_mvp.md` - MVP endpoint specifications
- **Interactive API Docs**: http://localhost:8000/docs (when server is running)

## Database Models

Core entities implemented:
- **Standards** - Educational standards for content generation
- **Products** - Generated content items (worksheets, passages, quizzes)
- **Generation Jobs** - Content generation tasks
- **Upload Tasks** - VA team workflow tasks
- **File Artifacts** - Generated files and metadata

## Tech Stack

- **FastAPI** - Modern web framework
- **SQLAlchemy** - ORM with declarative models
- **Alembic** - Database migrations
- **PostgreSQL** - Database
- **Pydantic v2** - Data validation and serialization
- **Uvicorn** - ASGI server

## Development Workflow

1. **Day 1**: Foundation setup ✅
2. **Day 2**: Core entities and API scaffolding ✅
3. **Day 3+**: Business logic implementation
4. **Future**: AI integration, n8n workflows, authentication

## Project Structure Notes

- **Modular Design**: Clear separation between API, models, schemas, services
- **Type Safety**: Full type hints with Pydantic v2
- **Database**: SQLAlchemy models with proper indexing
- **API Versioning**: v1 namespace for future compatibility
- **Documentation**: Comprehensive docs for team alignment
