"""
Pruebas unitarias para el recomendador TF-IDF de PequeLectores.

Estas pruebas validan que el pipeline de ML (TF-IDF + similitud coseno)
funciona correctamente, incluyendo todos los casos borde especificados.

Conceptos probados:
  - Inicialización del vectorizador TF-IDF
  - Construcción del corpus de libros
  - Cálculo de puntuaciones con similitud coseno
  - Generación de explicaciones (XAI)
  - Ordenamiento y filtrado de resultados
"""

import sys
import os

# Agregar el directorio backend al path para importar el módulo
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import pytest  # noqa: E402
import numpy as np  # noqa: E402
from app.services.recommender import TFIDFRecommender  # noqa: E402


# ---------------------------------------------------------------------------
# Datos de prueba (fixtures)
# ---------------------------------------------------------------------------

@pytest.fixture
def sample_books():
    """Libros de ejemplo para las pruebas, con formato real de OpenLibrary."""
    return [
        {
            "key": "/works/OL123W",
            "title": "Harry Potter and the Sorcerer's Stone",
            "author": "J.K. Rowling",
            "subject": ["fantasy", "magic", "wizards", "hogwarts"],
            "cover_url": None,
            "first_publish_year": 1997,
        },
        {
            "key": "/works/OL456W",
            "title": "The Hobbit",
            "author": "J.R.R. Tolkien",
            "subject": ["fantasy", "adventure", "dragons", "elves"],
            "cover_url": None,
            "first_publish_year": 1937,
        },
        {
            "key": "/works/OL789W",
            "title": "Charlotte's Web",
            "author": "E.B. White",
            "subject": ["animals", "friendship", "pigs", "spiders"],
            "cover_url": None,
            "first_publish_year": 1952,
        },
        {
            "key": "/works/OL101W",
            "title": "Percy Jackson: The Lightning Thief",
            "author": "Rick Riordan",
            "subject": ["fantasy", "greek gods", "adventure", "magic"],
            "cover_url": None,
            "first_publish_year": 2005,
        },
        {
            "key": "/works/OL202W",
            "title": "A Brief History of Time",
            "author": "Stephen Hawking",
            "subject": ["science", "physics", "universe", "astronomy"],
            "cover_url": None,
            "first_publish_year": 1988,
        },
    ]


@pytest.fixture
def sample_books_no_subject():
    """Libro sin temas (subject) para probar casos borde."""
    return [
        {
            "key": "/works/OL999W",
            "title": "Mystery Book Without Subjects",
            "author": "Unknown Author",
            "subject": [],
            "cover_url": None,
            "first_publish_year": 2000,
        }
    ]


@pytest.fixture
def sample_books_no_author():
    """Libro sin autor para probar casos borde."""
    return [
        {
            "key": "/works/OL888W",
            "title": "Anonymous Masterpiece",
            "author": None,
            "subject": ["mystery", "thriller"],
            "cover_url": None,
            "first_publish_year": 1999,
        }
    ]


# ---------------------------------------------------------------------------
# Prueba 1: El constructor crea el vectorizador correctamente
# ---------------------------------------------------------------------------

class TestInit:
    """Pruebas de inicialización del recomendador."""

    def test_init_creates_vectorizer(self):
        """
        Verifica que al crear una instancia de TFIDFRecommender:
        - El vectorizador existe (no es None).
        - Tiene la configuración correcta: max_features=500,
          stop_words='english', ngram_range=(1,2).
        """
        rec = TFIDFRecommender()
        assert rec.vectorizer is not None, (
            "El vectorizador debería estar inicializado"
        )
        assert rec.vectorizer.max_features == 500, (
            "Debe limitarse a 500 características para evitar ruido"
        )
        assert rec.vectorizer.stop_words == "english", (
            "Debe usar stop words en inglés para filtrar palabras vacías"
        )
        assert rec.vectorizer.ngram_range == (1, 2), (
            "Debe usar unigramas y bigramas para capturar frases compuestas"
        )


# ---------------------------------------------------------------------------
# Prueba 2 y 3: Construcción del corpus
# ---------------------------------------------------------------------------

class TestBuildCorpus:
    """Pruebas de construcción del corpus de texto."""

    def test_build_corpus_combines_fields(self, sample_books):
        """
        Verifica que _build_corpus concatena correctamente título,
        autor y temas de cada libro en un solo string.
        """
        rec = TFIDFRecommender()
        corpus = rec._build_corpus(sample_books)

        assert len(corpus) == len(sample_books), (
            "El corpus debe tener un elemento por cada libro"
        )
        # El primer libro debe contener palabras de título, autor y temas
        first_text = corpus[0].lower()
        assert "harry" in first_text or "potter" in first_text, (
            "El corpus debe incluir el título del libro"
        )
        assert "rowling" in first_text, (
            "El corpus debe incluir el autor del libro"
        )
        assert "fantasy" in first_text and "magic" in first_text, (
            "El corpus debe incluir los temas (subjects) del libro"
        )

    def test_build_corpus_handles_missing_fields(
        self, sample_books_no_subject, sample_books_no_author
    ):
        """
        Verifica que _build_corpus maneja correctamente libros
        sin temas (subject) y sin autor.

        Casos borde:
          - Libro sin subject: usa solo título + autor.
          - Libro sin autor: usa solo título + subject.
        """
        rec = TFIDFRecommender()

        # Caso 1: libro sin temas
        corpus_no_subj = rec._build_corpus(sample_books_no_subject)
        assert len(corpus_no_subj) == 1, "Debe generar un elemento del corpus"
        text_no_subj = corpus_no_subj[0].lower()
        assert "mystery book without subjects" in text_no_subj, (
            "Debe incluir el título aunque no tenga temas"
        )

        # Caso 2: libro sin autor
        corpus_no_auth = rec._build_corpus(sample_books_no_author)
        assert len(corpus_no_auth) == 1, "Debe generar un elemento del corpus"
        text_no_auth = corpus_no_auth[0].lower()
        assert "anonymous masterpiece" in text_no_auth, (
            "Debe incluir el título aunque no tenga autor"
        )
        assert "mystery" in text_no_auth or "thriller" in text_no_auth, (
            "Debe incluir los temas aunque no tenga autor"
        )


# ---------------------------------------------------------------------------
# Pruebas 4-7: Puntuación de libros (score_books)
# ---------------------------------------------------------------------------

class TestScoreBooks:
    """Pruebas del método principal de puntuación."""

    def test_score_books_returns_scored_list(self, sample_books):
        """
        Verifica que score_books devuelve una lista de libros con
        los campos 'score' y 'explanation' añadidos.

        Para una consulta relacionada con fantasy, los libros de
        ese género deben recibir puntuación > 0.
        """
        rec = TFIDFRecommender()
        queries = ["fantasy", "magic", "dragons"]

        scored = rec.score_books(sample_books, queries)

        assert len(scored) == len(sample_books), (
            "Debe devolver la misma cantidad de libros que recibe"
        )
        for book in scored:
            assert "score" in book, (
                "Cada libro debe tener el campo 'score'"
            )
            assert "explanation" in book, (
                "Cada libro debe tener el campo 'explanation' (XAI)"
            )
            assert isinstance(book["score"], float), (
                "El score debe ser un número flotante"
            )
            assert 0.0 <= book["score"] <= 1.0, (
                f"El score debe estar entre 0 y 1, pero es {book['score']:.4f}"
            )

    def test_score_books_higher_for_match(self, sample_books):
        """
        Verifica que los libros cuyo contenido coincide con la consulta
        reciben puntuaciones más altas que libros no relacionados.

        Consulta: ['animals', 'pigs', 'spiders'] → Charlotte's Web
        debería tener mayor score que A Brief History of Time.
        """
        rec = TFIDFRecommender()
        queries = ["animals", "pigs", "spiders"]

        scored = rec.score_books(sample_books, queries)

        # Charlotte's Web (índice 2) trata sobre animales, arañas, cerdos
        charlotte_score = scored[2]["score"]

        # A Brief History of Time (índice 4) trata de ciencia
        hawking_score = scored[4]["score"]

        assert charlotte_score > hawking_score, (
            f"Charlotte's Web ({charlotte_score:.4f}) debería tener mayor "
            f"puntuación que A Brief History of Time ({hawking_score:.4f}) "
            f"para la consulta sobre animales"
        )

    def test_score_books_empty_books(self):
        """
        Caso borde: lista de libros vacía.
        score_books debe devolver una lista vacía sin fallar.
        """
        rec = TFIDFRecommender()
        result = rec.score_books([], ["fantasy", "magic"])
        assert result == [], (
            "Con lista vacía de libros debe devolver lista vacía"
        )

    def test_score_books_empty_queries(self, sample_books):
        """
        Caso borde: lista de consultas vacía.
        score_books debe devolver todos los libros con score 0.0.
        """
        rec = TFIDFRecommender()
        result = rec.score_books(sample_books, [])

        assert len(result) == len(sample_books), (
            "Debe devolver todos los libros"
        )
        for book in result:
            assert book["score"] == 0.0, (
                "Sin consultas, todos los scores deben ser 0.0"
            )
            assert book["explanation"] == "", (
                "Sin consultas, no debe haber explicación"
            )

    def test_score_books_single_book(self):
        """
        Caso borde: un solo libro en el corpus (REQ-006).
        Con menos de 2 libros el TF-IDF no tiene sentido
        (IDF sería constante). Debe devolver score 0.0.
        """
        rec = TFIDFRecommender()
        single_book = [{
            "key": "/works/OL1W",
            "title": "El Único Libro",
            "author": "Autor Solitario",
            "subject": ["aventura", "fantasía"]
        }]
        result = rec.score_books(single_book, ["aventura"])
        
        assert len(result) == 1, "Debe devolver el único libro"
        assert result[0]["score"] == 0.0, (
            "Con un solo libro, el score debe ser 0.0"
        )

    def test_score_books_missing_subjects(self, sample_books):
        """
        Caso borde: libro sin campo 'subject' (REQ-005).
        score_books debe funcionar usando solo título y autor
        para los libros que no tienen subjects.
        """
        rec = TFIDFRecommender()
        # Crear una copia con un libro sin subjects
        books_with_gaps = [dict(b) for b in sample_books]
        books_with_gaps[0] = {
            "key": "/works/OL99W",
            "title": "Libro Sin Temas",
            "author": "Autor Anónimo",
            "subject": []  # subjects vacío
        }
        
        result = rec.score_books(books_with_gaps, ["fantasy", "magic"])
        
        assert len(result) == len(sample_books), (
            "Debe devolver todos los libros incluso si alguno no tiene subjects"
        )
        # El libro sin subjects tiene score (basado en título + autor)
        assert "score" in result[0], (
            "El libro sin subjects debe tener campo score"
        )


# ---------------------------------------------------------------------------
# Prueba 8: Explicabilidad (XAI)
# ---------------------------------------------------------------------------

class TestExplain:
    """Pruebas del módulo de explicabilidad (XAI)."""

    def test_explain_returns_top_words(self, sample_books):
        """
        Verifica que _explain devuelve un string con hasta 3 palabras
        que contribuyeron a la puntuación del libro.

        Para una consulta sobre "fantasy magic", la explicación debe
        contener términos del libro que coincidieron con la consulta.
        """
        rec = TFIDFRecommender()
        queries = ["fantasy", "magic"]

        # Ejecutar score_books para obtener la matriz TF-IDF y explicaciones
        scored = rec.score_books(sample_books, queries)

        # Harry Potter (índice 0) tiene subjects: fantasy, magic, wizards
        hp_explanation = scored[0]["explanation"]
        assert isinstance(hp_explanation, str), (
            "La explicación debe ser un string"
        )
        # Debe contener al menos un término relevante
        assert len(hp_explanation) > 0, (
            "Un libro que coincide con la consulta debe tener explicación"
        )

        # Charlotte's Web (índice 2) no coincide → explicación vacía o irrelevante
        charlotte_explanation = scored[2]["explanation"]
        # No podemos garantizar que esté vacía (depende del vocabulario TF-IDF),
        # pero su score debe ser bajo
        assert scored[2]["score"] < scored[0]["score"], (
            "Charlotte's Web debe tener menor score que Harry Potter "
            "para consulta de fantasy"
        )


# ---------------------------------------------------------------------------
# Pruebas 9-10: Ordenamiento y filtrado (get_top_recommendations)
# ---------------------------------------------------------------------------

class TestGetTopRecommendations:
    """Pruebas del método get_top_recommendations."""

    def test_get_top_recommendations_sorted(self, sample_books):
        """
        Verifica que get_top_recommendations devuelve los libros
        ordenados de mayor a menor puntuación (score descendente).

        El primer libro de la lista debe tener score >= al segundo,
        y así sucesivamente.
        """
        rec = TFIDFRecommender()
        queries = ["fantasy", "magic", "dragons"]

        top = rec.get_top_recommendations(sample_books, queries)

        # Verificar orden descendente
        scores = [book["score"] for book in top]
        for i in range(len(scores) - 1):
            assert scores[i] >= scores[i + 1], (
                f"Posición {i}: score {scores[i]:.4f} debe ser >= "
                f"score {scores[i+1]:.4f} (orden descendente)"
            )

    def test_get_top_recommendations_respects_top_n(self, sample_books):
        """
        Verifica que get_top_recommendations respeta el parámetro top_n
        y no devuelve más libros de los solicitados.
        """
        rec = TFIDFRecommender()
        queries = ["fantasy"]

        # Pedir solo 2 recomendaciones de 5 libros disponibles
        top_2 = rec.get_top_recommendations(sample_books, queries, top_n=2)

        assert len(top_2) == 2, (
            f"Debe devolver exactamente 2 libros, pero devolvió {len(top_2)}"
        )

        # Pedir más de los disponibles
        top_20 = rec.get_top_recommendations(sample_books, queries, top_n=20)
        assert len(top_20) == len(sample_books), (
            "Si top_n > cantidad de libros, debe devolver todos los disponibles"
        )

        # top_n=0 debe devolver lista vacía
        top_0 = rec.get_top_recommendations(sample_books, queries, top_n=0)
        assert len(top_0) == 0, (
            "top_n=0 debe devolver lista vacía"
        )
