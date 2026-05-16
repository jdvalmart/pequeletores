# 🎓 Guía Completa: PequeLectores desde Cero

> **Para:** Profesores, compañeros, y cualquier persona sin conocimientos técnicos previos.  
> **Objetivo:** Entender qué es PequeLectores, cómo funciona, y cómo construimos la IA.

---

## 📖 Índice

1. [¿Qué es PequeLectores?](#1-qué-es-pequeletores)
2. [¿Por qué lo hicimos?](#2-por-qué-lo-hicimos)
3. [¿Qué hace la aplicación?](#3-qué-hace-la-aplicación)
4. [Las piezas del sistema](#4-las-piezas-del-sistema)
5. [La magia: ¿cómo funciona la IA?](#5-la-magia-cómo-funciona-la-ia)
6. [Explicación técnica de la IA (paso a paso)](#6-explicación-técnica-de-la-ia-paso-a-paso)
7. [¿Dónde está funcionando?](#7-dónde-está-funcionando)
8. [¿Qué aprendimos?](#8-qué-aprendimos)
9. [Glosario: palabras técnicas explicadas](#9-glosario)

---

## 1. ¿Qué es PequeLectores?

**PequeLectores es una página web que recomienda libros a niños usando Inteligencia Artificial.**

Imagina que un niño de 8 años entra a una biblioteca con 5,000 libros. ¿Cómo sabe cuál elegir? PequeLectores resuelve eso: el niño selecciona íconos de cosas que le gustan (dragones, espacio, fútbol, hadas...) y el sistema busca automáticamente los mejores libros para él, explicándole por qué se los recomienda.

**No es solo una lista de libros. Es un sistema inteligente que:**
- 🎨 Deja que el niño exprese sus gustos con dibujos (no con texto)
- 🧠 Usa matemáticas e IA para encontrar los libros más compatibles
- 💬 Explica por qué recomendó cada libro
- 🏆 Motiva al niño con juegos: rachas e insignias

---

## 2. ¿Por qué lo hicimos?

### El problema real:

> *"Mamá, no sé qué libro leer."*  
> *"Papá, todos los libros se ven iguales."*  
> *"Profe, ¿este libro es para mi edad?"*

Los niños entre 6 y 14 años enfrentan tres barreras gigantes para leer:

1. **Demasiadas opciones** — una biblioteca o librería tiene miles de libros. Es abrumador.
2. **No saben buscar** — no conocen autores, géneros ni palabras clave para encontrar lo que les gusta.
3. **Falta de motivación** — sin alguien que los guíe, pierden el interés rápido.

Los papás y profesores también sufren: no siempre saben qué libro es apropiado para la edad del niño.

### Nuestra solución:

PequeLectores elimina esas tres barreras:

| Barrera | Cómo la resolvemos |
|---------|-------------------|
| Demasiadas opciones | La IA filtra y muestra solo los 10 mejores libros |
| No saben buscar | El niño solo toca íconos, no escribe nada |
| Falta de motivación | Rachas, insignias y puntajes como un videojuego |

---

## 3. ¿Qué hace la aplicación?

### Pantalla 1: Inicio 🏠

El niño ve:
- Su **racha de lectura** actual (🔥 3 días seguidos)
- Botones para: Elegir intereses, Ver recomendaciones, Mi perfil

### Pantalla 2: Elegir Intereses 🎨

El niño ve **36 íconos** organizados en categorías:
- 🐾 **Animales:** perro, gato, dinosaurio, caballo, dragón, mariposa
- 🚀 **Aventura:** cohete, brújula, montaña, barco, tesoro, mapa
- 🧙 **Fantasía:** mago, hada, fantasma, magia, castillo, corona
- 🔬 **Ciencia:** ciencia, tierra, estrella, robot, cerebro, bombilla
- ⚽ **Deportes:** fútbol, baloncesto, natación, bicicleta, trofeo, medalla
- 😂 **Diversión:** risa, arte, música, juego, cámara, corazón

Toca los que le gustan (máximo 5) y presiona "¡Ver Recomendaciones!"

### Pantalla 3: Recomendaciones 📚

El sistema muestra **10 libros** ordenados del más al menos compatible. Cada libro muestra:
- 🖼️ La portada del libro
- 📝 Título y autor
- 📊 **Porcentaje de compatibilidad** (ej: 41%)
- 💬 **Explicación:** "Recomendado por: dragons, fantasy, adventure"

El niño también puede marcar "¡Ya leí este libro!" para ganar páginas.

### Pantalla 4: Mi Perfil 👤

El niño ve:
- 🔥 Su racha actual y su récord
- 🏆 Insignias ganadas y las que le faltan
- 📊 Estadísticas: libros leídos, páginas leídas, insignias

---

## 4. Las piezas del sistema

Piensa en PequeLectores como un **restaurante**:

| Pieza | Analogía | ¿Qué hace? |
|-------|----------|------------|
| 🖥️ **Frontend** | El mesero y el menú | Lo que el niño ve y toca en la pantalla |
| 🧠 **Backend** | El chef en la cocina | Recibe el pedido, cocina la respuesta |
| 💾 **Base de datos** | La nevera y despensa | Guarda gustos, libros leídos, insignias |
| 🤖 **Motor de IA** | La receta secreta | Decide qué libros recomendar |
| 📚 **Open Library** | El mercado | De donde sacamos los ingredientes (datos de libros) |

### ¿Cómo se comunican?

```
1. Niño toca "dragón" en la app
2. Frontend: "Backend, el niño quiere dragones"
3. Backend: "Motor IA, busca libros de dragones"
4. Motor IA: "Open Library, dame libros sobre dragones"
5. Open Library: "Aquí tienes 20 libros sobre dragones"
6. Motor IA: "De estos 20, estos 10 son los mejores para este niño"
7. Backend: "Frontend, muestra estos 10 libros"
8. Frontend: "Niño, mira estos libros que te van a encantar"
```

---

## 5. La magia: ¿cómo funciona la IA?

### Primero, entendamos el problema:

Tienes 60 libros y un niño que ama los dragones, el espacio y el fútbol. ¿Cómo encuentras los 10 libros más parecidos a sus gustos?

Un humano lo haría así:
1. Leería el título de cada libro
2. Leería los temas de cada libro
3. Compararía mentalmente: "Este habla de dragones, este de cocina... el de dragones le va a gustar más"

**La IA hace exactamente lo mismo, pero con matemáticas.**

### La idea clave: convertir palabras en números

Las computadoras no entienden palabras. Solo entienden números.

Entonces, ¿cómo le decimos a una computadora que "dragón" y "fantasía" son parecidos?

**Convirtiendo las palabras en números.** Esto se llama **vectorización.**

Imagina que cada palabra es una coordenada en un mapa:

```
        dragón (0.8)
        │
        │   🐉 Libro 1: "Eragon"
        │  (dragón=0.8, cocina=0.0, espacio=0.1)
        │
        ──────────────────── cocina (0.0)
        │
        │   🍳 Libro 2: "Recetas Fáciles"
        │  (dragón=0.0, cocina=0.9, espacio=0.0)
```

- El Libro 1 está cerca de "dragón" y lejos de "cocina"
- El Libro 2 está cerca de "cocina" y lejos de "dragón"
- Si el niño ama los dragones, el Libro 1 es mejor recomendación

Esto es una simplificación con 2 dimensiones. Nuestro sistema usa **500 dimensiones** (500 palabras diferentes).

---

## 6. Explicación técnica de la IA (paso a paso)

### Paso 1: De íconos a palabras

El niño selecciona 🐉 y 🚀. El sistema traduce:

| Ícono | Palabras de búsqueda |
|-------|---------------------|
| 🐉 dragón | "dragons", "fantasy" |
| 🚀 espacio | "space", "astronauts", "science fiction" |

**Total: 5 palabras de búsqueda**

---

### Paso 2: Buscar libros en internet

Usamos **Open Library**, una biblioteca gratuita de internet con millones de libros. Buscamos libros que contengan esas 5 palabras en sus temas.

Resultado: ~60 libros, cada uno con:
- Título (ej: "His Majesty's Dragon")
- Autor (ej: "Naomi Novik")
- Temas (ej: ["dragons", "fantasy", "adventure", "war"])

---

### Paso 3: TF-IDF — Convertir libros en números

**TF-IDF** significa *Term Frequency - Inverse Document Frequency* (Frecuencia de Término - Frecuencia Inversa de Documento).

Suena complicado, pero la idea es simple:

- **TF (Term Frequency):** ¿Cuántas veces aparece una palabra en ESTE libro?  
  *"dragons" aparece 15 veces en "Eragon" → valor alto*

- **IDF (Inverse Document Frequency):** ¿En cuántos libros aparece esta palabra?  
  *"dragons" aparece en 3 de 60 libros → es una palabra RARA y VALIOSA*  
  *"the" aparece en 58 de 60 libros → es una palabra COMÚN y POCO VALIOSA*

**TF-IDF = TF × IDF**

Resultado: una tabla de 60 filas (libros) × 500 columnas (palabras importantes).

```
           dragons  fantasy  cooking  space  the
Libro 1:    0.8      0.6      0.0     0.1   0.0
Libro 2:    0.0      0.0      0.9     0.0   0.0
Libro 3:    0.3      0.7      0.0     0.5   0.0
...
Libro 60:   0.0      0.0      0.0     0.8   0.0
```

Cada fila es un **vector** — una lista de 500 números que representa un libro.

---

### Paso 4: Vectorizar los gustos del niño

Tomamos las 5 palabras de búsqueda ("dragons fantasy space astronauts science fiction") y las convertimos en un vector usando las MISMAS 500 palabras.

```
Vector del niño:  [0.7, 0.5, 0.0, 0.6, 0.0, ...]
                    ↑    ↑         ↑
                  dragón fantasía  espacio
```

---

### Paso 5: Similitud coseno — Comparar vectores

Ahora tenemos:
- 60 vectores de libros (cada uno de 500 números)
- 1 vector del niño (500 números)

**Similitud coseno** mide el ángulo entre dos vectores:
- Si apuntan en la misma dirección (ángulo 0°) → **similitud = 1.0** (100% compatible)
- Si son perpendiculares (ángulo 90°) → **similitud = 0.0** (0% compatible)
- Si apuntan en direcciones opuestas (ángulo 180°) → **similitud = -1.0** (totalmente diferente)

```
Niño:  [dragons=0.7, fantasy=0.5, cooking=0.0, space=0.6]
Libro: [dragons=0.8, fantasy=0.6, cooking=0.0, space=0.1]
              ↑↑            ↑↑                    ↑↑
        Misma dirección en dragons y fantasy → ¡Alta similitud!

Niño:  [dragons=0.7, fantasy=0.5, cooking=0.0]
Libro: [dragons=0.0, fantasy=0.0, cooking=0.9]
              ≠             ≠              ≠
        Direcciones opuestas → ¡Baja similitud!
```

Calculamos la similitud coseno entre el vector del niño y cada uno de los 60 vectores de libros. Obtenemos 60 números entre 0 y 1.

---

### Paso 6: Ranking y Top 10

Ordenamos los 60 libros del que tiene mayor similitud al menor. Nos quedamos con los 10 primeros.

---

### Paso 7: XAI — Explicar por qué

**XAI = Explainable AI (IA Explicable)**

No queremos una "caja negra" que diga "lee este libro" sin explicar por qué. Nuestro sistema analiza cuáles fueron las 3 palabras que más contribuyeron al puntaje de cada libro.

```
Libro: "His Majesty's Dragon" — Score: 0.41
Explicación: "dragons, fantasy, adventure"

Esto significa:
- La palabra "dragons" contribuyó ~0.15 al score
- La palabra "fantasy" contribuyó ~0.13 al score
- La palabra "adventure" contribuyó ~0.08 al score
```

---

### Resumen visual del pipeline completo:

```
🎨 Niño elige íconos
    ↓
🔤 Traducción a palabras clave
    ↓
📚 Búsqueda en Open Library (60 libros)
    ↓
🔢 TF-IDF: cada libro → vector de 500 números
    ↓
🔢 TF-IDF: gustos del niño → vector de 500 números
    ↓
📐 Similitud coseno: 60 comparaciones
    ↓
📊 Ranking: ordenar por score
    ↓
🏆 Top 10 + explicación XAI
    ↓
🖥️ Mostrar en la pantalla
```

---

## 7. ¿Dónde está funcionando?

El sistema NO está solo en nuestra computadora. Está **vivo en internet:**

| ¿Qué? | ¿Dónde? | ¿Quién lo provee? |
|--------|---------|-------------------|
| La página web | [pequeletores.netlify.app](https://pequeletores.netlify.app) | Netlify (gratis) |
| El cerebro (API) | [pequeletores-production.up.railway.app](https://pequeletores-production.up.railway.app) | Railway (gratis) |
| Base de datos | Vincular a Railway | Railway PostgreSQL |
| Código fuente | [github.com/jdvalmart/pequeletores](https://github.com/jdvalmart/pequeletores) | GitHub |

### ¿Qué significa "desplegar"?

"Desplegar" significa **subir el código a internet para que cualquiera pueda usarlo.** No necesitas instalar nada en tu computadora. Así funciona:

1. Escribimos código en nuestra computadora
2. Lo subimos a GitHub
3. Railway y Netlify lo detectan automáticamente
4. En ~2 minutos, los cambios están disponibles para todo el mundo

---

## 8. ¿Qué aprendimos?

### Conceptos de IA que aplicamos:

| Concepto | ¿Qué es? | ¿Dónde lo usamos? |
|----------|----------|-------------------|
| **TF-IDF** | Técnica para medir importancia de palabras en documentos | Convertir libros en vectores numéricos |
| **Vectorización** | Transformar texto en números | Representar libros y gustos como listas de números |
| **Similitud Coseno** | Medir qué tan parecidos son dos vectores | Comparar gustos del niño con cada libro |
| **Content-Based Filtering** | Recomendar basado en características del contenido | Todo el sistema de recomendación |
| **XAI** | IA que explica sus decisiones | Mostrar por qué se recomendó cada libro |

### Retos reales que enfrentamos:

1. **Datos incompletos** — Muchos libros en OpenLibrary no tienen temas (subjects) o tienen información faltante. En el mundo real, limpiar datos es el 80% del trabajo de IA.

2. **Sinónimos** — TF-IDF no entiende que "dragón" y "bestia alada" son lo mismo. Para eso se necesitan técnicas más avanzadas como Word2Vec o transformers.

3. **Rendimiento** — Con 60 libros el sistema es rápido (10 milisegundos). Con 100,000 libros necesitaríamos optimizaciones.

---

## 9. Glosario

### Términos técnicos explicados en español simple:

| Término | Explicación |
|---------|-------------|
| **API** | *Application Programming Interface.* Es como un mesero: el frontend le pide datos al backend, y el backend los entrega. |
| **Backend** | La parte del sistema que no se ve. Procesa datos, se conecta a la base de datos, ejecuta la IA. |
| **Base de datos** | Donde se guarda la información permanentemente (gustos de niños, libros leídos, insignias). |
| **CORS** | *Cross-Origin Resource Sharing.* Un sistema de seguridad que controla quién puede hablar con el backend. |
| **Cosine Similarity** | Fórmula matemática que mide el ángulo entre dos vectores. Si es 1, son idénticos. Si es 0, no tienen nada en común. |
| **Desplegar (Deploy)** | Subir el código a internet para que funcione en un servidor real, no solo en tu computadora. |
| **Docker** | Herramienta que empaqueta el backend en una "caja" que funciona igual en cualquier computadora. |
| **Frontend** | La parte visual de la aplicación. Lo que el usuario ve y toca. |
| **JWT** | *JSON Web Token.* Un "carnet digital" que prueba que ya iniciaste sesión, sin necesidad de volver a poner contraseña. |
| **Open Library** | Biblioteca digital gratuita con millones de libros. Nosotros solo leemos sus datos, no los modificamos. |
| **Pipeline** | Una serie de pasos en orden. Como una línea de ensamblaje: entra un dato, pasa por varias etapas, sale un resultado. |
| **PostgreSQL** | Tipo de base de datos profesional, gratuita y muy usada en la industria. |
| **Python** | Lenguaje de programación. Fácil de leer, muy usado en IA y ciencia de datos. |
| **React** | Herramienta para construir interfaces web interactivas. Creada por Facebook. |
| **scikit-learn** | Biblioteca de Python con herramientas de IA listas para usar. Nosotros usamos su TF-IDF y cosine similarity. |
| **Score** | Puntaje numérico. En nuestro sistema, qué tan compatible es un libro con los gustos del niño (0 = nada, 1 = perfecto). |
| **TF-IDF** | Fórmula que mide la importancia de una palabra: qué tanto aparece en un libro vs en todos los libros. |
| **Vector** | Lista de números que representa algo. Un libro se convierte en un vector de 500 números. |
| **XAI** | *Explainable AI.* IA que no solo da un resultado, sino que explica cómo llegó a él. |
| **Ícono** | Dibujo que representa un interés (ej: 🐉 = dragones, ⚽ = deportes). |

---

> **Documento preparado por:**  
> Juan David Valencia · Mireya Traslaviña · Elena Lucumi  
> *Bootcamp MINTIC IA — 2026*
