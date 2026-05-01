# Tasks: Pequelectores_mvp

## Phase 1: Infrastructure (✅ Complete)

- [x] 1.1 Setup monorepo with backend/ and frontend/ directories
- [x] 1.2 Create docker-compose.yaml with PostgreSQL 15 service
- [x] 1.3 Setup FastAPI app with CORS middleware
- [x] 1.4 Configure SQLAlchemy async engine with postgresql+asyncpg
- [x] 1.5 Create database.py with connection pool
- [x] 1.6 Setup Alembic for migrations
- [x] 1.7 Add environment config in .env files

## Phase 2: Backend Core (✅ Complete)

- [x] 2.1 Create child model (id, name, birth_date, age)
- [x] 2.2 Create child_preferences model (child_id, icon_ids, created_at)
- [x] 2.3 Create reading_log model (child_id, book_id, pages_read, logged_at)
- [x] 2.4 Create badge model (id, name, description, icon, requirement)
- [x] 2.5 POST /preferences endpoint
- [x] 2.6 GET /recommendations endpoint
- [x] 2.7 POST /reading/log endpoint
- [x] 2.8 GET /streaks endpoint
- [x] 2.9 GET /badges endpoint
- [x] 2.10 Open Library client with cache
- [x] 2.11 TF-IDF recommender service
- [x] 2.12 Startup badge seeding

## Phase 3: Frontend Core (✅ Complete)

- [x] 3.1 Init React + Vite + TypeScript project
- [x] 3.2 Create API client (axios wrapper)
- [x] 3.3 Create IconPicker component
- [x] 3.4 Create BookCard component
- [x] 3.5 Create Home page with streak display
- [x] 3.6 Create Preferences page with IconPicker form
- [x] 3.7 Create Recommendations page with BookCard grid
- [x] 3.8 Create Profile page with badges + stats

## Phase 4: Integration (✅ Complete)

- [x] 4.1 Connect Preferences page to /preferences API
- [x] 4.2 Connect Recommendations page to /recommendations API
- [x] 4.3 Connect Home page to /reading/log POST on book click
- [x] 4.4 Connect Profile page to /streaks and /badges APIs
- [x] 4.5 Seed demo child on startup

## Phase 5: Testing (✅ Complete)

- [x] 5.1 Unit tests for backend recommender service (TF-IDF)
- [x] 5.2 Unit tests for TF-IDF vectorization logic
- [x] 5.3 Integration test: full recommendation flow

---

## Project Complete! 🎉

All 34 tasks completed successfully.