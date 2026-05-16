# 📚 PequeLectores — Recomendación de Libros con IA

> **Bootcamp MINTIC IA — Proyecto Final**  
> Una página web que recomienda libros a niños usando Inteligencia Artificial.

---

## 👥 Equipo

| Integrante | Rol | ¿Qué hizo? |
|------------|-----|-------------|
| **Juan David Valencia** | Lead Developer / Backend | El "cerebro" del sistema: API, base de datos, y el motor de IA |
| **Mireya Traslaviña** | Frontend Developer / UX | La "cara" del sistema: diseño, interfaz, experiencia del usuario |
| **Elena Lucumi** | QA Engineer / Testing | La "calidad": pruebas, validación, asegurar que todo funcione |

---

## 🎯 ¿Qué problema resolvemos?

Los niños entre 6 y 14 años muchas veces **no encuentran libros que les gusten**. Entran a una biblioteca o librería, ven cientos de libros y no saben cuál elegir. Los papás tampoco saben qué recomendarles.

**Nuestra solución:**
- 🎨 El niño **elige íconos** de lo que le gusta (🐉 dragones, 🚀 espacio, ⚽ deportes...)
- 🧠 Una **Inteligencia Artificial** analiza sus gustos y busca libros parecidos
- 🏆 El sistema lo **motiva con juegos**: rachas de lectura e insignias por logros

> *En palabras simples: es como Netflix, pero para libros infantiles.*

---

## 🏗️ ¿Cómo está construido?

Imagina el sistema como un restaurante:

| Parte | ¿Qué es? | Tecnología |
|-------|----------|------------|
| 🖥️ **Frontend** | Lo que el niño ve en la pantalla (botones, íconos, colores) | React + TypeScript |
| 🧠 **Backend** | El "cerebro" que procesa los datos y toma decisiones | FastAPI + Python |
| 💾 **Base de Datos** | Donde se guarda todo (gustos del niño, libros leídos, insignias) | PostgreSQL |
| 🤖 **Motor de IA** | El que decide qué libros recomendar analizando palabras | scikit-learn (TF-IDF) |
| 📚 **Open Library** | Una biblioteca gratuita de internet de donde sacamos los libros | API externa |

**Diagrama simplificado:**
```
 Niño usa la app → Frontend pide libros → Backend consulta IA
                                                    ↓
    IA analiza gustos y busca en Open Library → Devuelve los 10 mejores libros
```

---

## 🚀 ¿Dónde está funcionando?

El sistema está **vivo en internet**, no solo en una computadora:

| ¿Qué? | ¿Dónde? |
|--------|---------|
| **La página web** | [pequeletores.netlify.app](https://pequeletores.netlify.app) |
| **El cerebro (API)** | [pequeletores-production.up.railway.app](https://pequeletores-production.up.railway.app) |

Cada vez que subimos código a GitHub, el sistema se actualiza solo en ambos lugares.

---

## 🧠 ¿Cómo funciona la Inteligencia Artificial?

> *Imagina que tienes una biblioteca con 60 libros. ¿Cómo encuentras los 10 que más le gustarían a un niño que ama los dragones y el espacio?*

### Paso a paso (explicado sin tecnicismos):

```
1. El niño elige 🐉 dragón y 🚀 espacio
        ↓
2. Traducimos los íconos a palabras: "dragons", "fantasy", "space", "astronauts"
        ↓
3. Buscamos en internet 60 libros que hablen de esos temas
        ↓
4. Convertimos cada libro en una lista de números (un "vector")
   - Cada número representa qué tan importante es una palabra en ese libro
   - Ejemplo: para "dragons", el libro "His Majesty's Dragon" recibe un número alto
        ↓
5. Convertimos los gustos del niño en otra lista de números (otro "vector")
        ↓
6. Comparamos los vectores con "similitud coseno"
   - Si apuntan en la misma dirección → el libro es muy relevante (score alto)
   - Si apuntan en direcciones opuestas → el libro no tiene nada que ver (score bajo)
        ↓
7. Ordenamos los 60 libros del más al menos relevante
        ↓
8. Mostramos los 10 mejores, explicando POR QUÉ cada uno:
   "Este libro salió porque contiene: dragons, fantasy, adventure"
```

### Los 3 conceptos de IA que usamos:

| Concepto | Explicación simple | Ejemplo |
|----------|-------------------|---------|
| **TF-IDF** | Mide qué tan importante es una palabra en un libro comparado con todos los demás. "Dragón" es muy importante en un libro de dragones, pero "el" o "la" no importan porque salen en todos. | La palabra "dragons" pesa mucho en *Eragon*, pero "the" pesa casi nada |
| **Similitud Coseno** | Compara si dos listas de números "apuntan" en la misma dirección. No importa qué tan largas sean las listas, sino hacia dónde van. | Niño: [dragons=0.8, space=0.6, cooking=0.0] vs Libro: [dragons=0.9, space=0.1, cooking=0.0] → ¡Muy parecidos! |
| **XAI** | Inteligencia Artificial Explicable: en vez de ser una "caja negra", nuestro sistema TE DICE por qué recomendó cada libro. | "Recomendado por: dragons, fantasy, adventure" |

### Ejemplo de lo que el niño ve:

```
📚 His Majesty's Dragon    → 41% compatible | Por: dragons, fantasy
📚 Dragonsong              → 28% compatible | Por: dragons, fantasy  
📚 No children, no pets    → 28% compatible | Por: pets
```

---

## 🛠️ Tecnologías que usamos

| Categoría | Herramienta | ¿Para qué sirve? |
|-----------|-------------|------------------|
| **Interfaz visual** | React, TypeScript | Lo que el usuario ve y toca en la pantalla |
| **Lógica del sistema** | FastAPI, Python | El cerebro que procesa las peticiones |
| **Almacenamiento** | PostgreSQL | Guarda usuarios, gustos, libros leídos |
| **Inteligencia Artificial** | scikit-learn | La parte que "piensa" y recomienda |
| **Seguridad** | JWT + bcrypt | Contraseñas protegidas y acceso seguro |
| **Calidad** | pytest, Vitest | Pruebas automáticas para que nada se rompa |

---

## 🏆 ¿Cómo motivamos a los niños a leer?

### 🔥 Rachas de lectura
El sistema cuenta cuántos días seguidos ha leído el niño. Si lee hoy y mañana, tiene una racha de 2 días. Si falla un día, la racha vuelve a cero. ¡Como el Snapchat de la lectura!

### 🏅 Insignias por logros

| Insignia | ¿Cuándo se gana? |
|----------|------------------|
| 📖 First Pages | Leer 10 páginas |
| 📚 Chapter One | Leer 50 páginas |
| 🔖 Bookworm | Leer 100 páginas |
| 🎓 Avid Reader | Leer 500 páginas |
| 🏆 Reading Champion | Leer 1000 páginas |
| 👑 Legendary Reader | Leer 5000 páginas |
| ⭐ First Book | Terminar el primer libro |
| 🧭 Explorer | Leer libros de 3 temas diferentes |

---

## 📚 Lo que Aprendimos de IA

### ✅ Qué aplicamos del bootcamp
- **TF-IDF** — cómo medir la importancia de una palabra en un texto. No es lo mismo "dragón" (importante, sale poco) que "el" (irrelevante, sale en todos lados).
- **Vectorización** — cómo convertir palabras en números para que una computadora las entienda.
- **Similitud coseno** — cómo comparar gustos con libros sin buscar palabras exactas, sino "direcciones" en un espacio matemático.
- **Content-Based Filtering** — recomendar basándonos en el CONTENIDO del libro (sus temas), no en lo que otros usuarios leyeron.
- **XAI** — no solo decir "lee este libro", sino explicar POR QUÉ.

### ⚠️ Retos que enfrentamos
- **Datos sucios** — muchos libros en internet tienen información incompleta. Aprendimos que limpiar datos es el 80% del trabajo en IA.
- **TF-IDF no entiende sinónimos** — "dragón" y "bestia alada" son lo mismo para un humano, pero para la máquina son palabras distintas. Eso se resuelve con embeddings o transformers.
- **Simplicidad vs potencia** — para un proyecto académico, TF-IDF es perfecto porque se ENTIENDE y se EXPLICA. Modelos más complejos existen, pero son "cajas negras".

### 🔜 ¿Qué seguiría después?
- Que el sistema **aprenda de lo que el niño ya leyó** (feedback)
- **Recomendar sin conocer gustos** (cold start: por edad o popularidad)
- **Medir qué tan buenas son las recomendaciones** (métricas: precision, recall)

---

## 🧪 ¿Cómo probarlo en tu computadora?

```bash
# 1. Base de datos
docker-compose up -d

# 2. Backend (el cerebro)
cd backend
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000

# 3. Frontend (la página web)
cd frontend
npm install
npm run dev
```

Luego abre `http://localhost:5173` en tu navegador.

---

## 📄 Licencia

MIT — Proyecto académico Bootcamp MINTIC IA 2026.

---

> **Juan Valencia · Mireya Traslaviña · Elena Lucumi**  
> *"Porque cada niño merece encontrar su próximo libro favorito"* 📚
