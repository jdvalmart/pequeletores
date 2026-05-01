# PequeLectores Inteligente por IA

Book recommendation system for children (ages 6-14) with AI-powered recommendations and gamification.

## Stack

- **Frontend**: React + TypeScript + Vite + Vitest
- **Backend**: FastAPI (Python async) + SQLAlchemy
- **Database**: PostgreSQL
- **ML**: scikit-learn (TF-IDF)
- **Testing**: pytest (backend), Vitest (frontend)

## Quick Start

### 1. Start PostgreSQL

```bash
docker-compose up -d
```

### 2. Setup Backend

```bash
cd backend
python -m venv venv
source venv/bin/activate  # Linux/Mac
pip install -r requirements.txt

# Configure environment
cp .env.production .env  # For production, or use .env for development

uvicorn app.main:app --reload --port 8000
```

### 3. Setup Frontend

```bash
cd frontend
npm install
npm run dev
```

### 4. Run Tests (Optional)

```bash
# Backend tests
cd backend && pytest --cov

# Frontend tests
cd frontend && npm test
```

## API Endpoints

### Authentication
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | /api/auth/register | Register new parent |
| POST | /api/auth/login | Login parent |
| GET | /api/auth/me | Get current parent |

### Preferences
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | /api/preferences | Save child preferences |
| GET | /api/preferences/{child_id} | Get child preferences |

### Recommendations
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | /api/recommendations | Get book recommendations |

### Reading Activity
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | /api/reading/log | Log reading activity |
| GET | /api/reading/streak/{child_id} | Get streak |

### Badges
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | /api/badges | Get all badges |
| GET | /api/badges/{child_id} | Get child's badges |

## Features

- 🎨 Visual preference selection (icon picker)
- 📚 Book recommendations via TF-IDF
- 🔥 Reading streaks
- 🏆 Badge system
- 📖 Open Library integration
- 🔐 Parent authentication (JWT)
- ✅ Full test coverage (backend + frontend)

## Environment Variables

### Backend (.env)

```bash
# Database
DATABASE_URL=postgresql+asyncpg://user:pass@localhost:5433/pequena_lectores

# App Settings
DEBUG=true
ENVIRONMENT=development

# Server
BACKEND_HOST=0.0.0.0
BACKEND_PORT=8000

# CORS
CORS_ORIGINS=http://localhost:5173,http://localhost:3000

# Auth (change in production!)
SECRET_KEY=your-secret-key
```

### Backend (.env.production) - Production Template

```bash
DEBUG=false
ENVIRONMENT=production
DATABASE_URL=postgresql+asyncpg://prod-url
SECRET_KEY=<generate-secure-key>
CORS_ORIGINS=https://your-domain.com
```

### Frontend (.env)

```bash
VITE_API_URL=http://localhost:8000
```

## Project Structure

```
PequeLectores_inteligente_por_IA/
├── backend/
│   ├── app/
│   │   ├── api/routes/    # API endpoints
│   │   ├── models/        # SQLAlchemy models
│   │   ├── services/      # Business logic
│   │   ├── middleware/    # Error handlers
│   │   └── config.py      # Settings
│   ├── tests/             # Backend tests
│   └── requirements.txt
├── frontend/
│   ├── src/
│   │   ├── api/          # API client
│   │   ├── components/   # React components
│   │   ├── pages/        # Page components
│   │   ├── types/        # TypeScript types
│   │   └── schemas/      # Zod schemas
│   ├── tests/            # Frontend tests
│   └── package.json
└── docker-compose.yml
```

## License

MIT