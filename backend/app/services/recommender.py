"""
Servicio recomendador de libros basado en contenido (content-based).

Utiliza TF-IDF (Term Frequency - Inverse Document Frequency) de scikit-learn
para vectorizar los libros y las preferencias del usuario, y similitud coseno
para calcular qué tan relevante es cada libro para una consulta dada.

Conceptos clave de ML explicados:
  - TF-IDF: Mide la importancia de una palabra en un documento relativa
    a una colección de documentos. Penaliza palabras muy frecuentes (stop words)
    y premia palabras distintivas.
  - Similitud coseno: Mide el ángulo entre dos vectores en espacio n-dimensional,
    sin importar su magnitud. Valores cercanos a 1 indican alta similitud.
"""

from typing import Any

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np


class TFIDFRecommender:
    """Recomendador de libros usando TF-IDF y similitud coseno.

    Esta clase implementa un sistema de recomendación basado en contenido
    (content-based filtering) que compara los temas, títulos y autores de
    los libros con las preferencias del usuario usando procesamiento de texto.

    Flujo del algoritmo:
      1. Construir un corpus de texto a partir de los libros (título + autor + temas)
      2. Vectorizar el corpus con TF-IDF → matriz libro-palabra
      3. Vectorizar la consulta del usuario con el mismo vocabulario
      4. Calcular similitud coseno entre consulta y cada libro
      5. Ordenar por puntuación y devolver los mejores N
    """

    def __init__(self):
        """Inicializa el recomendador con el vectorizador TF-IDF.

        Configuración del vectorizador:
          - max_features=500: Limita el vocabulario a las 500 palabras más
            frecuentes para evitar ruido y reducir dimensionalidad.
          - stop_words='english': Elimina palabras vacías (the, a, is, etc.)
            que no aportan significado semántico.
          - ngram_range=(1,2): Considera palabras individuales (unigramas)
            y pares de palabras consecutivas (bigramas) para capturar
            frases como "science fiction" o "greek gods".
        """
        self.vectorizer = TfidfVectorizer(
            max_features=500,
            stop_words='english',
            ngram_range=(1, 2)
        )

    def _build_corpus(self, books: list[dict[str, Any]]) -> list[str]:
        """Construye un corpus de texto a partir de los metadatos de los libros.

        Para cada libro concatena su título, autor y temas en un solo string.
        Esto permite que el TF-IDF capture relaciones entre estos campos.

        Casos borde manejados:
          - Libro sin temas (subject): usa solo título + autor.
          - Libro sin autor: usa solo título + temas.
          - Libro sin autor ni temas: usa solo el título.

        Args:
            books: Lista de diccionarios de libros con claves
                   'title', 'author', 'subject'.

        Returns:
            Lista de strings, uno por libro, con el texto concatenado.
        """
        corpus = []
        for book in books:
            partes = []

            # Título: siempre presente como identificador principal
            title = book.get("title", "")
            if title:
                partes.append(title)

            # Autor: añade contexto sobre el estilo literario
            author = book.get("author")
            if author:
                partes.append(str(author))

            # Temas: las palabras más relevantes para la recomendación
            subjects = book.get("subject", [])
            if subjects:
                # Unir todos los temas en un solo string
                partes.append(" ".join(subjects))

            # Unir todas las partes con espacios
            texto = " ".join(partes) if partes else ""
            corpus.append(texto)

        return corpus

    def score_books(
        self, books: list[dict[str, Any]], queries: list[str]
    ) -> list[dict[str, Any]]:
        """Puntúa libros según su relevancia a las consultas del usuario.

        Este es el método principal del recomendador. Implementa los
        siguientes pasos del pipeline de ML:

        1. Construye el corpus de libros con _build_corpus()
        2. Ajusta (fit) el vectorizador TF-IDF al corpus de libros
        3. Transforma la consulta del usuario al mismo espacio vectorial
        4. Calcula la similitud coseno entre la consulta y cada libro
        5. Genera una explicación textual con las palabras más relevantes

        Mecanismo de explicabilidad (XAI):
          Para cada libro, el método _explain() identifica las palabras
          que más contribuyeron a la puntuación, haciendo el sistema
          transparente y auditable por los profesores.

        Args:
            books: Lista de diccionarios de libros.
            queries: Lista de términos de búsqueda del usuario
                     (ej: ['fantasy', 'magic', 'dragons']).

        Returns:
            Lista de libros con campos 'score' (float 0-1) y
            'explanation' (str) añadidos a cada diccionario original.
        """
        # Caso borde: menos de 2 libros — no tiene sentido calcular
        # TF-IDF con un solo documento (el IDF sería constante).
        if not books or len(books) < 2:
            return [{**b, "score": 0.0, "explanation": ""} for b in books]

        # Caso borde: sin consultas — no hay qué comparar.
        if not queries:
            return [{**b, "score": 0.0, "explanation": ""} for b in books]

        # Paso 1: Construir el corpus de texto de los libros
        corpus = self._build_corpus(books)

        # Paso 2: Ajustar TF-IDF al corpus y transformarlo a matriz
        # tfidf_matrix[i, j] = importancia de la palabra j en el libro i
        tfidf_matrix = self.vectorizer.fit_transform(corpus)

        # Paso 3: Transformar la consulta al mismo espacio vectorial
        # Unimos todas las queries en un solo texto de búsqueda
        query_text = " ".join(queries)
        query_vec = self.vectorizer.transform([query_text])

        # Paso 4: Calcular similitud coseno entre consulta y cada libro
        # cosine_similarity devuelve una matriz [1 x N] donde N = cantidad de libros
        sims = cosine_similarity(query_vec, tfidf_matrix).flatten()

        # Obtener nombres de características (palabras del vocabulario)
        feature_names = self.vectorizer.get_feature_names_out()

        # Paso 5: Construir resultados con puntuación y explicación
        scored_books = []
        for i, book in enumerate(books):
            score = float(sims[i])
            explanation = self._explain(
                i, tfidf_matrix, feature_names, query_vec
            )
            # Crear copia del libro con score y explicación
            scored_books.append({
                **book,
                "score": score,
                "explanation": explanation
            })

        return scored_books

    def _explain(
        self,
        idx: int,
        matrix: np.ndarray,
        feature_names: list[str],
        query_vec: np.ndarray
    ) -> str:
        """Genera una explicación textual de por qué un libro fue recomendado.

        Identifica las 3 palabras que más contribuyeron a la puntuación
        de similitud coseno para un libro específico.

        Método: multiplica elemento a elemento el vector de la consulta
        por el vector del libro. Los términos con mayor producto son los
        que más peso tienen en el numerador de la similitud coseno
        (producto punto). Esto es una aproximación de la contribución
        real, suficientemente precisa para fines educativos.

        Args:
            idx: Índice del libro en la matriz TF-IDF.
            matrix: Matriz TF-IDF de documentos [n_libros x n_palabras].
            feature_names: Nombres de las características (palabras).
            query_vec: Vector TF-IDF de la consulta [1 x n_palabras].

        Returns:
            String con hasta 3 palabras separadas por coma,
            o string vacío si no hay contribuciones detectables.
        """
        # Extraer el vector del libro específico
        book_vec = matrix[idx].toarray().flatten()

        # Extraer el vector de la consulta
        query_arr = query_vec.toarray().flatten()

        # Producto elemento a elemento: contribución de cada término
        # Términos donde ambos vectores tienen valor alto = alta contribución
        contribution = book_vec * query_arr

        # Obtener índices de los 3 términos con mayor contribución
        top_indices = contribution.argsort()[::-1][:3]

        # Construir la explicación con los nombres de los términos
        top_terms = [
            str(feature_names[i])
            for i in top_indices
            if contribution[i] > 0  # Solo incluir términos con contribución real
        ]

        return ", ".join(top_terms) if top_terms else ""

    def get_top_recommendations(
        self,
        books: list[dict[str, Any]],
        queries: list[str],
        top_n: int = 10
    ) -> list[dict[str, Any]]:
        """Obtiene los N mejores libros recomendados ordenados por puntuación.

        Este método envuelve score_books() y añade ordenamiento descendente
        por score más recorte al top N.

        Args:
            books: Lista de diccionarios de libros.
            queries: Lista de términos de consulta del usuario.
            top_n: Cantidad máxima de recomendaciones a devolver.
                   Por defecto 10.

        Returns:
            Lista de hasta top_n libros ordenados de mayor a menor
            puntuación, cada uno con campos 'score' y 'explanation'.
        """
        # Obtener libros puntuados
        scored = self.score_books(books, queries)

        # Ordenar descendente por puntuación (mayor score primero)
        scored.sort(key=lambda x: x.get("score", 0.0), reverse=True)

        # Devolver solo los top N
        return scored[:top_n]
