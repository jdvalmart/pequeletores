# 📚 PequeLectores — Recomendación de Libros con IA

> **Bootcamp MINTIC IA — Proyecto Final**  
> Sistema de recomendación de libros para niños usando Inteligencia Artificial y gamificación.

---

## 👥 Equipo

| Integrante | Rol | Responsabilidades |
|------------|-----|-------------------|
| **Juan David Valencia** | Lead Developer / Backend | Arquitectura, API REST, motor de IA, DevOps |
| **Mireya Traslaviña** | Frontend Developer / UX | Interfaz de usuario, diseño responsivo, experiencia visual |
| **Elena Lucumi** | QA Engineer / Testing | Pruebas unitarias, integración, validación de calidad |

---

## 🎯 El Problema

Los niños entre 6 y 14 años frecuentemente **no encuentran libros que les interesen**, lo que reduce su motivación por la lectura. Los padres y tutores enfrentan dificultades para identificar títulos apropiados.

**PequeLectores resuelve esto con:**
- 🎨 **Selección visual de intereses** — el niño elige íconos (🐉 dragones, 🚀 espacio, ⚽ deportes)
- 🧠 **IA real** — TF-IDF + similitud coseno para recomendar libros personalizados
- 🏆 **Gamificación** — rachas de lectura e insignias que motivan a seguir leyendo

---

## 🏗️ Arquitectura

```
┌──────────────────────────────────────────────────┐
│              FRONTEND (Netlify)                   │
│  React + TypeScript + Vite                        │
│  https://pequeletores.netlify.app                 │
└────────────────────┬─────────────────────────────┘
                     │ HTTPS
┌────────────────────▼─────────────────────────────┐
│              BACKEND (Railway)                    │
│  FastAPI + Python 3.14 + scikit-learn            │
│  https://pequeletores-production.up.railway.app   │
└────────────────────┬─────────────────────────────┘
                     │ asyncpg
┌────────────────────▼─────────────────────────────┐
│           PostgreSQL 15 (Railway)                 │
│  Tablas: children, preferences, reading_logs      │
└──────────────────────────────────────────────────┘
                     │ HTTP
┌────────────────────▼─────────────────────────────┐
│           Open Library API (externo)              │
│  Datos de libros: título, autor, portada, temas   │
└──────────────────────────────────────────────────┘
```

---

## 🚀 Despliegue

| Entorno | URL | Rama |
|---------|-----|------|
| **Frontend** | https://pequeletores.netlify.app | `main` |
| **Backend API** | https://pequeletores-production.up.railway.app | `main` |

- **GitHub Push → Railway** — auto-deploy backend con Docker
- **GitHub Push → Netlify** — auto-deploy frontend con `npm run build`

---

## 🧠 ¿Cómo funciona la IA?

### Pipeline de Recomendación (Content-Based Filtering)

```
1. Niño selecciona íconos  ──→  ["🐉", "🚀", "⚽"]
2. Íconos → queries         ──→  ["dragons", "fantasy", "space", "sports"]
3. OpenLibrary search       ──→  60 libros con título, autor, temas
4. TF-IDF vectorization     ──→  Matriz numérica libros × palabras
5. Cosine similarity        ──→  Score 0..1 por libro
6. Top 10 + XAI             ──→  "Recomendado por: dragons, fantasy"
```

### Tecnologías de IA utilizadas

| Concepto | Herramienta | ¿Qué hace? |
|----------|-------------|-----------|
| **TF-IDF** | `TfidfVectorizer` (scikit-learn) | Convierte texto de libros en vectores numéricos, midiendo importancia de cada palabra |
| **Similitud Coseno** | `cosine_similarity` (scikit-learn) | Compara el vector de preferencias del niño con cada libro |
| **XAI** | Algoritmo propio | Explica qué palabras contribuyeron más a cada recomendación |

### Ejemplo real (producción)

```
📚 His Majesty's Dragon    → score: 0.41 | dragons, fantasy
📚 Dragonsong              → score: 0.28 | dragons, fantasy  
📚 No children, no pets    → score: 0.28 | pets
```

---

## 🛠️ Stack Tecnológico

| Capa | Tecnología | Versión |
|------|-----------|---------|
| **Frontend** | React, TypeScript, Vite | 18 / 5.3 / 5.0 |
| **Backend** | FastAPI, Python | 0.115 / 3.14 |
| **Base de Datos** | PostgreSQL + SQLAlchemy async | 15 / 2.0 |
| **IA/ML** | scikit-learn (TF-IDF), numpy | 1.4 / 1.26 |
| **Auth** | JWT (python-jose) + bcrypt | 3.3 / 4.0 |
| **Testing** | pytest, Vitest, React Testing Library | 8.0 / 1.2 / 14.1 |
| **DevOps** | Docker, Railway, Netlify, GitHub | — |

---

## 🏆 Sistema de Gamificación

### Rachas (Streaks)
- 🔥 Días consecutivos de lectura
- 🏅 Récord personal guardado

### Insignias (Badges)

| Insignia | Páginas requeridas | Icono |
|----------|-------------------|-------|
| First Pages | 10 | 📖 |
| Chapter One | 50 | 📚 |
| Bookworm | 100 | 🔖 |
| Avid Reader | 500 | 🎓 |
| Reading Champion | 1000 | 🏆 |
| Legendary Reader | 5000 | 👑 |
| First Book | 1 libro | ⭐ |
| Explorer | 3 materias diferentes | 🧭 |

---

## 📂 Estructura del Proyecto

```
PequeLectores_inteligente_por_IA/
├── backend/
│   ├── app/
│   │   ├── api/
│   │   │   ├── deps.py              # Dependencias FastAPI (DB session)
│   │   │   └── routes/
│   │   │       ├── auth.py          # Registro/login JWT
│   │   │       ├── preferences.py   # Preferencias del niño
│   │   │       ├── recommendations.py # Motor de recomendación
│   │   │       ├── reading.py       # Registro de lectura + streaks
│   │   │       └── gamification.py  # Badges e insignias
│   │   ├── middleware/
│   │   │   └── errors.py            # Manejo global de errores
│   │   ├── models/                  # Modelos SQLAlchemy
│   │   ├── services/
│   │   │   ├── recommender.py       # 🧠 IA: TF-IDF + cosine similarity
│   │   │   ├── openlibrary.py       # Cliente Open Library API
│   │   │   └── auth.py              # Servicio de autenticación
│   │   ├── config.py                # Configuración con pydantic-settings
│   │   ├── database.py              # Conexión async a PostgreSQL
│   │   └── main.py                  # Punto de entrada FastAPI
│   ├── tests/                       # Tests backend (pytest)
│   ├── Dockerfile                   # Imagen para Railway
│   └── requirements.txt
├── frontend/
│   ├── src/
│   │   ├── api/client.ts            # Cliente HTTP tipado
│   │   ├── components/              # BookCard, StreakCounter, IconPicker...
│   │   ├── pages/                   # Home, Preferences, Recommendations, Profile
│   │   ├── types/                   # Tipos TypeScript
│   │   └── schemas/                 # Validación Zod
│   ├── tests/                       # Tests frontend (Vitest)
│   └── package.json
├── netlify.toml                     # Configuración Netlify
├── railway.json                     # Configuración Railway
└── docker-compose.yml               # PostgreSQL local
```

---

## 🧪 Desarrollo Local

```bash
# 1. PostgreSQL
docker-compose up -d

# 2. Backend
cd backend
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000

# 3. Frontend
cd frontend
npm install
npm run dev
```

---

## 📚 Lo que Aprendimos

### ✅ Qué funcionó bien
- **TF-IDF + cosine similarity** — enfoque simple pero efectivo para recomendaciones basadas en contenido
- **FastAPI async** — rendimiento excelente con PostgreSQL async
- **Railway + Netlify** — despliegue continuo sin configuración compleja
- **SDD (Spec-Driven Development)** — planificar antes de codear evitó retrabajo

### ⚠️ Retos encontrados
- **CORS en producción** — coordinar orígenes entre Netlify y Railway requirió ajustes
- **Datetimes aware vs naive** — asyncpg de PostgreSQL no mezcla timezone-aware con naive
- **OpenLibrary API** — datos inconsistentes (libros sin subjects, covers rotos)
- **Balance código académico vs producción** — mantenerlo simple pero funcional

### 🔜 Próximos pasos
- Frontend de autenticación (login/registro)
- CRUD de perfiles de niños (múltiples niños por padre)
- Proteger rutas con JWT
- Dashboard de padres con progreso de lectura

---

## 📄 Licencia

MIT — Proyecto académico Bootcamp MINTIC IA 2026.

---

> **Juan Valencia · Mireya Traslaviña · Elena Lucumi**  
> *"Porque cada niño merece encontrar su próximo libro favorito"* 📚
