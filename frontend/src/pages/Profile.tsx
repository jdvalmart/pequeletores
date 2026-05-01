import { useNavigate } from 'react-router-dom'
import { useQuery, useQueryClient } from '@tanstack/react-query'
import { StreakCounter } from '../components/StreakCounter'
import { BadgeDisplay } from '../components/BadgeDisplay'
import { getStreak, getChildBadges } from '../api/client'
import './Profile.css'

const DEMO_CHILD_ID = 1

export function ProfilePage() {
  const navigate = useNavigate()
  const queryClient = useQueryClient()

  const { data: streakData } = useQuery({
    queryKey: ['streak', DEMO_CHILD_ID],
    queryFn: () => getStreak(DEMO_CHILD_ID),
    enabled: !!DEMO_CHILD_ID
  })

  const { data: badgesData } = useQuery({
    queryKey: ['badges', DEMO_CHILD_ID],
    queryFn: () => getChildBadges(DEMO_CHILD_ID),
    enabled: !!DEMO_CHILD_ID
  })

  const booksRead = streakData?.total_books || 0
  const pagesRead = streakData?.total_pages || 0
  const badgesEarned = badgesData?.total_earned || 0

  const handleHome = () => {
    queryClient.invalidateQueries({ queryKey: ['recommendations'] })
    navigate('/')
  }

  return (
    <div className="profile-page">
      <header className="page-header">
        <h1>👤 Mi Perfil</h1>
      </header>

      <section className="profile-section streak-section">
        <h2>🔥 Racha de Lectura</h2>
        <StreakCounter childId={DEMO_CHILD_ID} />
      </section>

      <section className="profile-section badges-section">
        <h2>🏆 Mis Insignias</h2>
        <BadgeDisplay childId={DEMO_CHILD_ID} />
      </section>

      <section className="profile-section stats-section">
        <h2>📊 Mis Estadísticas</h2>
        <div className="stats-grid">
          <div className="stat-item">
            <span className="stat-value">{booksRead}</span>
            <span className="stat-label">Libros Leídos</span>
          </div>
          <div className="stat-item">
            <span className="stat-value">{pagesRead}</span>
            <span className="stat-label">Páginas Leídas</span>
          </div>
          <div className="stat-item">
            <span className="stat-value">{badgesEarned}</span>
            <span className="stat-label">Insignias Ganadas</span>
          </div>
        </div>
      </section>

      <div className="profile-actions">
        <button className="home-btn" onClick={handleHome}>
          🏠 Ir al Inicio
        </button>
      </div>
    </div>
  )
}