import { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { useMutation, useQueryClient } from '@tanstack/react-query'
import { IconPicker } from '../components/IconPicker'
import { savePreferences } from '../api/client'
import './Preferences.css'

const DEMO_CHILD_ID = 1  // ID del niño Demo Reader en la base de datos

export function PreferencesPage() {
  const navigate = useNavigate()
  const queryClient = useQueryClient()
  const [selectedIcons, setSelectedIcons] = useState<string[]>([])
  
  const mutation = useMutation({
    mutationFn: () => savePreferences(DEMO_CHILD_ID, selectedIcons),
    onSuccess: async () => {
      // Invalidar caché ANTES de navegar y esperar a que termine
      await queryClient.invalidateQueries({ queryKey: ['recommendations'] })
      await queryClient.invalidateQueries({ queryKey: ['preferences', DEMO_CHILD_ID] })
      // Limpiar caché forzosamente
      queryClient.clear()
      navigate('/recommendations')
    },
    onError: () => {
      alert('¡Ups! No pudimos guardar tus intereses. Intenta de nuevo.')
    }
  })

  const handleSubmit = () => {
    if (selectedIcons.length === 0) {
      alert('¡Selecciona al menos un interés!')
      return
    }
    mutation.mutate()
  }

  const handleHome = () => {
    queryClient.invalidateQueries({ queryKey: ['recommendations'] })
    navigate('/')
  }

  return (
    <div className="preferences-page">
      <header className="page-header">
        <h1>🎨 ¿Qué te gusta?</h1>
        <p>¡Toca los iconos que te interesan!</p>
      </header>

      <IconPicker
        selectedIcons={selectedIcons}
        onChange={setSelectedIcons}
        maxSelection={5}
      />

      <div className="preferences-actions">
        <button
          className="home-btn"
          onClick={handleHome}
        >
          🏠 Ir al Inicio
        </button>
        <button
          className="submit-btn"
          onClick={handleSubmit}
          disabled={mutation.isPending || selectedIcons.length === 0}
        >
          {mutation.isPending ? 'Guardando...' : '¡Ver Recomendaciones! 🎁'}
        </button>
      </div>
    </div>
  )
}