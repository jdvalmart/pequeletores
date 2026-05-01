/089 m PequeLectores_inteligente_Por_IA/

# PequeLectores Inteligente por IA

## Documento de Presentación del Proyecto

---

## 1. INFORMACIÓN GENERAL DEL PROYECTO

### 1.1 Datos del Proyecto

| Campo                    | Descripción                                         |
| ------------------------ | --------------------------------------------------- |
| **Nombre del Proyecto**  | PequeLectores Inteligente por IA                    |
| **Tipo de Proyecto**     | Sistema de recomendación de libros con gamificación |
| **Fecha de Elaboración** | 30 de abril de 2026                                 |
| **Versión**              | 1.0.0                                               |

### 1.2 Integrantes del Equipo de Trabajo

| Nombre                | Rol Principal            |
| --------------------- | ------------------------ |
| **Juan Valencia**     | Lead Developer / Backend |
| **Mireya Traslaviña** | Frontend Developer / UX  |
| **Elena Lucumi**      | QA Engineer / Testing    |

---

## 2. DESCRIPCIÓN DEL PROYECTO

### 2.1 Resumen Ejecutivo

**PequeLectores** es una aplicación web diseñada para recomendar libros a niños entre 6 y 14 años, utilizando técnicas de inteligencia artificial (TF-IDF) para personalizar las recomendaciones según los intereses visuales de cada niño. El sistema incluye gamificación con streaks de lectura y badges para motivar a los jóvenes lectores.

### 2.2 Problema que Solve

Los niños entre 6 y 14 años frecuentemente no encuentran libros que les interesen, lo que reduce su motivación por la lectura. Los padres y tutores tienen dificultades para identificar títulos apropiados para la edad de sus hijos. Este proyecto solve este problema mediante:

- Un sistema de selección visual de intereses (iconos)
- Recomendaciones personalizadas basadas en IA
- Gamificación para mantener el compromiso de lectura

### 2.3 Stakeholders

| Stakeholder           | Interés          | Expectativa                            |
| --------------------- | ---------------- | -------------------------------------- |
| Niños (6-14 años)     | Usuarios finales | Encontrar libros divertidos fácilmente |
| Padres/Tutores        | Supervisión      | Ver progreso y gestionar perfiles      |
| Bibliotecas escolares | Promotion        | Aumentar uso de la colección           |

---

## 3. ALCANCE DEL PROYECTO

### 3.1 Funcionalidades Incluidas

#### Módulo de Autenticación

- ✅ Registro de padres/tutores con email y contraseña
- ✅ Inicio de sesión con JWT
- ✅ Gestión de perfiles de niños asociados

#### Módulo de Preferencias

- ✅ Selección visual de intereses mediante iconos
- ✅ Almacenamiento y actualización de preferencias
- ✅ Validación de iconos permitidos

#### Módulo de Recomendaciones

- ✅ Recomendaciones basadas en TF-IDF
- ✅ Integración con Open Library API
- ✅ Cover images y metadatos de libros

#### Módulo de Gamificación

- ✅ Sistema de streaks (días consecutivos de lectura)
- ✅ Sistema de badges por logros
- ✅ Registro de páginas leídas

### 3.2 Funcionalidades Excluidas (Fuera de Alcance)

- ❌ Modo multilingüe (español únicamente)
- ❌ Integración con redes sociales
- ❌ Compras de libros in-app
- ❌ Chat o comunicación entre usuarios
- ❌ Modo offline / PWA

---

## 4. REQUERIMIENTOS FUNCIONALES

### 4.1 Autenticación y Autorización

| ID    | Requerimiento                                                           | Prioridad |
| ----- | ----------------------------------------------------------------------- | --------- |
| RF-01 | El sistema debe permitir registrar padres con email y contraseña válida | Alta      |
| RF-02 | El sistema debe permitir iniciar sesión a padres registrados            | Alta      |
| RF-03 | El sistema debe generar tokens JWT válidos por 24 horas                 | Alta      |
| RF-04 | El sistema debe validar credenciales antes de permitir acceso           | Alta      |
| RF-05 | El sistema debe permitir cerrar sesión invalidando el token             | Media     |

### 4.2 Gestión de Niños

| ID    | Requerimiento                                            | Prioridad |
| ----- | -------------------------------------------------------- | --------- |
| RF-06 | Los padres deben poder crear perfiles de sus hijos       | Alta      |
| RF-07 | Los padres deben poder editar información de sus hijos   | Media     |
| RF-08 | Los niños deben poder seleccionar sus intereses visuales | Alta      |
| RF-09 | Cada niño debe tener preferencias independientes         | Alta      |

### 4.3 Sistema de Preferencias

| ID    | Requerimiento                                            | Prioridad |
| ----- | -------------------------------------------------------- | --------- |
| RF-10 | El sistema debe presentar mínimo 36 iconos de intereses  | Alta      |
| RF-11 | El usuario debe seleccionar entre 1 y 10 iconos          | Alta      |
| RF-12 | El sistema debe guardar preferencias en la base de datos | Alta      |
| RF-13 | El sistema debe validar que los iconos sean válidos      | Alta      |

### 4.4 Recomendaciones de Libros

| ID    | Requerimiento                                                  | Prioridad |
| ----- | -------------------------------------------------------------- | --------- |
| RF-14 | El sistema debe mostrar mínimo 10 recomendaciones              | Alta      |
| RF-15 | Las recomendaciones deben basarse en preferencias del niño     | Alta      |
| RF-16 | El sistema debe obtener datos de Open Library API              | Alta      |
| RF-17 | Las recomendaciones deben mostrar: título, autor, portada, año | Alta      |
| RF-18 | Las recomendaciones deben mostrar porcentaje de match          | Media     |

### 4.5 Registro de Lectura

| ID    | Requerimiento                                        | Prioridad |
| ----- | ---------------------------------------------------- | --------- |
| RF-19 | Los niños deben poder registrar páginas leídas       | Alta      |
| RF-20 | El sistema debe calcular el streak automáticamente   | Alta      |
| RF-21 | El sistema debe mostrar el streak actual y el récord | Alta      |
| RF-22 | El sistema debe verificar si se ganan nuevos badges  | Alta      |

### 4.6 Sistema de Badges

| ID    | Requerimiento                                         | Prioridad |
| ----- | ----------------------------------------------------- | --------- |
| RF-23 | El sistema debe tener 8 badges predefinidos           | Alta      |
| RF-24 | Los badges deben basarse en páginas leídas acumuladas | Alta      |
| RF-25 | El sistema debe mostrar badges obtenidos y pendientes | Alta      |
| RF-26 | Los badges deben tener iconos representativos         | Media     |

---

## 5. REQUERIMIENTOS NO FUNCIONALES

### 5.1 Rendimiento

| ID     | Requerimiento              | Criterio de Aceptación            |
| ------ | -------------------------- | --------------------------------- |
| RNF-01 | Tiempo de respuesta de API | < 200ms para 95% de peticiones    |
| RNF-02 | Tiempo de carga de página  | < 3 segundos en conexión estándar |
| RNF-03 | Recomendaciones generadas  | < 2 segundos para 20 libros       |

### 5.2 Seguridad

| ID     | Requerimiento           | Criterio de Aceptación                 |
| ------ | ----------------------- | -------------------------------------- |
| RNF-04 | Contraseñas encriptadas | Usar bcrypt con cost factor >= 12      |
| RNF-05 | Tokens JWT              | Expiración máxima de 24 horas          |
| RNF-06 | Validación de entrada   | Todos los inputs validados server-side |
| RNF-07 | CORS                    | Configuración por entorno              |

### 5.3 Escalabilidad

| ID     | Requerimiento | Criterio de Aceptación                   |
| ------ | ------------- | ---------------------------------------- |
| RNF-08 | Base de datos | Soporte para 1000+ niños simultáneos     |
| RNF-09 | API REST      | Diseño stateless para horizontal scaling |

### 5.4 Calidad de Código

| ID     | Requerimiento               | Criterio de Aceptación            |
| ------ | --------------------------- | --------------------------------- |
| RNF-10 | Cobertura de tests backend  | Mínimo 80%                        |
| RNF-11 | Cobertura de tests frontend | Componentes principales cubiertos |
| RNF-12 | Tipos TypeScript            | Sin tipos 'any' implícitos        |
| RNF-13 | Validación backend          | Pydantic con constraints          |

### 5.5 Usabilidad

| ID     | Requerimiento     | Criterio de Aceptación                       |
| ------ | ----------------- | -------------------------------------------- |
| RNF-14 | Diseño responsivo | Funcional en móvil y desktop                 |
| RNF-15 | Accesibilidad     | Nombres accesibles para lectores de pantalla |

### 5.6 Disponibilidad

| ID     | Requerimiento         | Criterio de Aceptación  |
| ------ | --------------------- | ----------------------- |
| RNF-16 | Uptime objetivo       | 99% en producción       |
| RNF-17 | Health check endpoint | GET /health responde OK |

---

## 6. ESTIMACIÓN DE TIEMPO

### 6.1 Distribución por Fase

| Fase       | Descripción                                     | Estimación    |
| ---------- | ----------------------------------------------- | ------------- |
| **Fase 1** | Configuración de infraestructura y dependencias | 16 horas      |
| **Fase 2** | Sistema de autenticación JWT                    | 24 horas      |
| **Fase 3** | Manejo de errores y validación                  | 16 horas      |
| **Fase 4** | Testing backend (TDD)                           | 24 horas      |
| **Fase 5** | Tipos y validación frontend                     | 20 horas      |
| **Fase 6** | Testing frontend                                | 20 horas      |
| **Fase 7** | Integración y polish                            | 16 horas      |
|            | **Total Desarrollo**                            | **136 horas** |

### 6.2 Distribución por Rol

| Rol                          | Horas    | Porcentaje |
| ---------------------------- | -------- | ---------- |
| Juan Valencia (Backend)      | 80 horas | 58.8%      |
| Mireya Traslaviña (Frontend) | 48 horas | 35.3%      |
| Elena Lucumi (Testing)       | 32 horas | 23.5%      |

### 6.3 Estimación de Testing

| Tipo de Testing           | Estimación   | Descripción                  |
| ------------------------- | ------------ | ---------------------------- |
| Unit Tests Backend        | 16 horas     | 13 tests para auth, services |
| Integration Tests Backend | 8 horas      | Tests de API endpoints       |
| Unit Tests Frontend       | 16 horas     | 35 tests componentes         |
| E2E Testing               | 8 horas      | flujos principales           |
| **Total Testing**         | **48 horas** |                              |

### 6.4 Cronograma Sugerido (4 semanas)

| Semana   | Actividad                    | Entregable                 |
| -------- | ---------------------------- | -------------------------- |
| Semana 1 | Fases 1-2 (Infra + Auth)     | Auth endpoints funcionando |
| Semana 2 | Fases 3-4 (Errores + Tests)  | Coverage 80%+ backend      |
| Semana 3 | Fases 5-6 (Types + Tests FE) | Frontend con tests         |
| Semana 4 | Fase 7 + QA                  | Entrega final              |

---

## 7. TECNOLOGÍAS UTILIZADAS

### 7.1 Stack Técnico

| Capa         | Tecnología            | Versión |
| ------------ | --------------------- | ------- |
| **Frontend** | React                 | 18.2.0  |
|              | TypeScript            | 5.3.3   |
|              | Vite                  | 5.0.8   |
|              | Vitest                | 1.2.0   |
|              | React Testing Library | 14.1.2  |
|              | Zod                   | 3.22.4  |
| **Backend**  | FastAPI               | 0.115.0 |
|              | Python                | 3.14    |
|              | SQLAlchemy            | 2.0.0   |
|              | PostgreSQL            | -       |
|              | pytest                | 8.0.0   |
|              | scikit-learn          | 1.4.0   |
| **Infra**    | Docker                | -       |
|              | JWT (python-jose)     | 3.3.0   |
|              | structlog             | 24.0.0  |

### 7.2 Arquitectura

```
┌─────────────────────────────────────────────────────────┐
│                    FRONTEND (React)                     │
│  Pages: Home, Preferences, Recommendations, Profile   │
│  Components: BookCard, StreakCounter, IconPicker       │
│  API Client: typed + error handling                     │
└─────────────────────────┬───────────────────────────────┘
                          │ HTTP/REST
┌─────────────────────────▼───────────────────────────────┐
│                   BACKEND (FastAPI)                     │
│  Routes: /auth/*, /preferences/*, /recommendations/*   │
│  Services: auth, recommender, openlibrary               │
│  Middleware: error handlers, logging                   │
└─────────────────────────┬───────────────────────────────┘
                          │
┌─────────────────────────▼───────────────────────────────┐
│                 DATABASE (PostgreSQL)                   │
│  Models: Parent, Child, ChildPreferences, ReadingLog    │
│  Tables: parents, children, badges, reading_logs       │
└─────────────────────────────────────────────────────────┘
```

---

## 8. CONCLUSIONES

### 8.1 Resultados Esperados

Al finalizar este proyecto, se habrá construido un sistema completo de recomendación de libros para niños que incluye:

1. ✅ Sistema de autenticación seguro con JWT
2. ✅ Interfaz de selección visual de intereses
3. ✅ Motor de recomendaciones basado en TF-IDF
4. ✅ Sistema de gamificación (streaks y badges)
5. ✅ Suite completa de tests (48 tests)
6. ✅ Documentación técnica y de usuario

### 8.2 Recomendaciones para Implementación

1. **Iniciar con testing**: Adoptar TDD desde el inicio del desarrollo
2. **Separar entornos**: Mantener configuración diferenciada dev/prod
3. **Monitoreo**: Implementar logging estructurado desde el inicio
4. **Feedback temprano**: Involucrar a usuarios finales (niños) tempranamente

---

## 9. ANEXOS

### A. Diagramas de Arquitectura

Ver sección 7.2 - Diagrama de arquitectura del sistema

### B. Endpoints API

Consultar README.md para lista completa de endpoints

### C. Validación de Entrada

- Backend: Pydantic con constraints
- Frontend: Zod schemas

---

**Documento preparado por el equipo de PequeLectores**

Juan Valencia | Mireya Traslaviña | Elena Lucumi

_30 de abril de 2026_

