# Proposal: Pequelectores_mvp

## Intent

Ayudar a niños (6-14 años) a encontrar libros que quieran leer basándose en sus intereses mediante un sistema de recomendación inteligente con interfaz gamificada.

## Scope

### In Scope
- API REST FastAPI con endpoints de libros
- Sistema de recomendación TF-IDF + Content-Based
- Interfaz React con selección visual de preferencias
- Base de datos PostgreSQL
- Gamificación básica (streaks, badges)
- Integración con Open Library API

### Out of Scope
- Collaborative filtering
- Autenticación de usuarios
- Leaderboards sociales
- Reseñas de libros
- Sistema de ML avanzado

## Approach

Content-Based Filtering con TF-IDF. Niño selecciona iconos visuales de intereses (géneros, personajes) → sistema busca libros similares con cosine similarity → recomienda top-N libros.

## Affected Areas

| Area | Impact | Description |
|------|--------|------------|
| backend/api/ | New | FastAPI endpoints |
| backend/ml/ | New | TF-IDF model |
| backend/db/ | New | PostgreSQL models |
| frontend/ | New | React components |

## Risks

| Risk | Likelihood | Mitigation |
|------|----------|----------|
| Metadata limitada de Open Library | Medium | Caching, fallback a Google Books |
| Engagement bajo | High | Gamificación desde día 1 |

## Success Criteria

- [ ] Niño puede seleccionar preferencias visuales
- [ ] Sistema recomienda mínimo 5 libros relevantes
- [ ] Streak de lectura funciona
- [ ] Primer badge se unlockea