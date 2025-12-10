# RBB Engine Backend

AI-powered curriculum generation backend built with FastAPI.

## Project Structure

```
backend/
├── app/
│   ├── api/
│   │   └── v1/
│   │       └── routes/
│   │           └── health.py          # Health check endpoint
│   ├── core/
│   │   ├── config.py                  # Config exports
│   │   └── settings.py                # Environment settings
│   ├── db/
│   │   ├── base.py                    # Model imports for Alembic
│   │   └── session.py                 # Database session management
│   ├── models/
│   │   ├── product.py                 # Product model
│   │   ├── job.py                     # Job model
│   │   └── __init__.py
│   ├── schemas/
│   │   ├── product.py                 # Product Pydantic schemas
│   │   ├── job.py                     # Job Pydantic schemas
│   │   └── __init__.py
│   ├── services/
│   │   └── __init__.py                # Business logic (Day 2+)
│   ├── utils/
│   │   ├── logger.py                  # Logging configuration
│   │   └── storage.py                 # File storage utilities
│   └── main.py                        # FastAPI app factory
├── migrations/                         # Alembic migrations
│   ├── env.py
│   └── script.py.mako
├── alembic.ini                        # Alembic configuration
├── requirements.txt                   # Python dependencies
├── .env.example                       # Environment template
└── README.md
```

## Setup Instructions

### 1. Create Virtual Environment

```bash
cd backend
python3 -m venv venv
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
alembic revision --autogenerate -m "Initial migration"
alembic upgrade head
```

### 6. Start Development Server

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

The API will be available at: http://localhost:8000

API documentation: http://localhost:8000/docs

## Available Endpoints

- `GET /api/health` - Health check endpoint

## Tech Stack

- **FastAPI** - Modern web framework
- **SQLAlchemy** - ORM
- **Alembic** - Database migrations
- **PostgreSQL** - Database
- **Pydantic** - Data validation
- **Uvicorn** - ASGI server

## Next Steps (Day 2+)

- Implement business logic in services/
- Add CRUD operations for products and jobs
- Integrate with n8n workflows
- Add authentication and authorization
- Implement AI agent pipeline integration
