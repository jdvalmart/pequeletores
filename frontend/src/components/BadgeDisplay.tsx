import { useQuery } from '@tanstack/react-query'
import { getChildBadges } from '../api/client'
import './BadgeDisplay.css'

interface BadgeDisplayProps {
  childId: number | string
}

interface Badge {
  id: number
  name: string
  description: string
  icon: string
  requirement: number
  earned_at?: string
}

export function BadgeDisplay({ childId }: BadgeDisplayProps) {
  const { data: response, isLoading } = useQuery({
    queryKey: ['badges', childId],
    queryFn: () => getChildBadges(childId),
    enabled: !!childId
  })

  if (isLoading) {
    return <div className="badge-skeleton">🏆 ...</div>
  }

  const earnedBadges = response?.earned || []
  const unearnedBadges = response?.unearned || []
  const allBadges = [...earnedBadges, ...unearnedBadges]

  if (allBadges.length === 0) {
    return (
      <div className="badge-empty">
        <span className="badge-empty-icon">📚</span>
        <p>Start reading to earn badges!</p>
      </div>
    )
  }

  return (
    <div className="badge-grid">
      {earnedBadges.map((badge: Badge) => (
        <div key={badge.id} className="badge-item badge-earned" title={badge.description}>
          <span className="badge-icon">{badge.icon}</span>
          <span className="badge-name">{badge.name}</span>
        </div>
      ))}
      {unearnedBadges.map((badge: Badge) => (
        <div key={badge.id} className="badge-item badge-locked" title={badge.description}>
          <span className="badge-icon">🔒</span>
          <span className="badge-name">{badge.name}</span>
        </div>
      ))}
    </div>
  )
}