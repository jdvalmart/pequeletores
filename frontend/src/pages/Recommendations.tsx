import { useEffect } from 'react'
import { useNavigate } from 'react-router-dom'
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query'
import { BookGrid } from '../components/BookCard'
import { getRecommendations, logReading } from '../api/client'
import type { BookWithScore } from '../types'
import './Recommendations.css'

const DEMO_CHILD_ID = 1  // ID del niño Demo Reader en la base de datos

export function RecommendationsPage() {
  const navigate = useNavigate()
  const queryClient = useQueryClient()

  const handleFinalizar = () => {
    // Limpiar toda la caché de recomendaciones
    queryClient.invalidateQueries({ queryKey: ['recommendations'] })
    queryClient.invalidateQueries({ queryKey: ['preferences', DEMO_CHILD_ID] })
    // Volver al inicio
    navigate('/')
  }
  
  const { data: response, isLoading, error, refetch } = useQuery({
    queryKey: ['recommendations', DEMO_CHILD_ID],
    queryFn: () => getRecommendations(DEMO_CHILD_ID, 10),
    enabled: !!DEMO_CHILD_ID,
    staleTime: 0,
    refetchOnMount: 'always',  // Siempre refetch al montar
    refetchOnWindowFocus: true  // También refetch al volver a la ventana
  })

  // Refetch automático cada vez que se monta el componente
  useEffect(() => {
    refetch()
  }, [])

  const books: BookWithScore[] = response?.recommendations?.map((book: BookWithScore) => ({
    ...book,
    author: book.author ? [book.author] : []
  })) || []

  const logMutation = useMutation({
    mutationFn: ({ bookKey, pages }: { bookKey: string; pages: number }) => 
      logReading(DEMO_CHILD_ID, bookKey, pages),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['streak', DEMO_CHILD_ID] })
      queryClient.invalidateQueries({ queryKey: ['badges', DEMO_CHILD_ID] })
      alert('¡Increíble! ¡Sigue leyendo! 📖 ¡Tú puedes!')
    },
    onError: () => {
      alert('¡Ups! No pudimos registrar tu lectura. Intenta de nuevo.')
    }
  })

  const handleLogReading = (bookKey: string, pages: number) => {
    logMutation.mutate({ bookKey, pages })
  }

  return (
    <div className="recommendations-page">
      <header className="page-header">
        <h1>📚 Tus Recomendaciones</h1>
        <p>¡Libros que pensamos que te van a encantar!</p>
      </header>

      {isLoading && (
        <div className="loading">
          <span className="loading-icon">📚</span>
          <p>Buscando los mejores libros para ti...</p>
        </div>
      )}

      {error && (
        <div className="error">
          <p>⚠️ Algo salió mal. ¡Intenta de nuevo más tarde!</p>
        </div>
      )}

      {books && books.length > 0 && (
        <>
          <BookGrid 
            books={books} 
            onLogReading={handleLogReading}
          />
          <div className="recommendations-actions">
            <button className="home-btn" onClick={handleFinalizar}>
              🏠 Ir al Inicio
            </button>
          </div>
        </>
      )}

      {!isLoading && !error && (!books || books.length === 0) && (
        <div className="empty">
          <p>😢 ¡Aún no hay recomendaciones!</p>
          <p className="hint">Ve a Preferencias y selecciona tus intereses primero.</p>
        </div>
      )}
    </div>
  )
}