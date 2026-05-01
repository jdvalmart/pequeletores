import { useNavigate } from 'react-router-dom'
import './BackButton.css'

interface BackButtonProps {
  to?: string
  label?: string
}

export function BackButton({ to, label = 'Atrás' }: BackButtonProps) {
  const navigate = useNavigate()

  const handleClick = () => {
    if (to) {
      navigate(to)
    } else {
      navigate(-1)
    }
  }

  return (
    <button className="back-button" onClick={handleClick}>
      <span className="back-icon">←</span>
      <span className="back-label">{label}</span>
    </button>
  )
}