# Todo Management Application

A single-user Todo management app with a Python FastAPI backend and React + TypeScript frontend.

## Tech Stack

| Layer | Technology |
|---|---|
| Frontend | React 18 + Vite + TypeScript |
| Backend | Python 3.11+ FastAPI |
| Database | SQL Server Express (local) |
| ORM | SQLAlchemy 2.x async + Alembic |

## Architecture

Strict **Route -> Service -> Repository** layering.

## Local Setup

### Backend

```bash
cd backend
python -m venv venv
source venv/Scripts/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env  # Edit with your DB credentials
alembic upgrade head
uvicorn app.main:app --reload --port 8000
```

### Frontend

```bash
cd frontend
npm install
npm run dev
```

Open http://localhost:5173

## API Docs

Once the backend is running: http://localhost:8000/docs
