import { Link } from 'react-router-dom'
import { StreakCounter } from '../components/StreakCounter'
import './Home.css'

const DEMO_CHILD_ID = 1

export function HomePage() {
  return (
    <div className="home-page">
      <header className="home-header">
        <h1>📚 PequeLectores</h1>
        <p className="tagline">¡Descubre tu próxima aventura literaria!</p>
      </header>

      <section className="streak-section">
        <StreakCounter childId={DEMO_CHILD_ID} />
      </section>

      <nav className="home-nav">
        <Link to="/preferences" className="nav-card choose-books">
          <span className="nav-icon">🎨</span>
          <span className="nav-label">Elige tus Intereses</span>
        </Link>
        
        <Link to="/recommendations" className="nav-card get-recommendations">
          <span className="nav-icon">📖</span>
          <span className="nav-label">Ver Recomendaciones</span>
        </Link>
        
        <Link to="/profile" className="nav-card my-profile">
          <span className="nav-icon">👤</span>
          <span className="nav-label">Mi Perfil</span>
        </Link>
      </nav>

      <section className="home-tip">
        <p>💡 <strong>Consejo:</strong> ¡Selecciona tus intereses para obtener mejores recomendaciones de libros!</p>
      </section>
    </div>
  )
}