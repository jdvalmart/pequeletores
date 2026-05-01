import { useQuery } from '@tanstack/react-query'
import { getStreak } from '../api/client'
import './StreakCounter.css'

interface StreakCounterProps {
  childId: string
}

export function StreakCounter({ childId }: StreakCounterProps) {
  const { data, isLoading } = useQuery({
    queryKey: ['streak', childId],
    queryFn: () => getStreak(childId),
    enabled: !!childId
  })

  if (isLoading) {
    return <div className="streak-skeleton">🔥 ...</div>
  }

  const streak = data?.current_streak || 0
  const longest = data?.longest_streak || 0

  return (
    <div className="streak-counter">
      <div className="streak-main">
        <span className="streak-fire">🔥</span>
        <span className="streak-number">{streak}</span>
        <span className="streak-label">días seguidos</span>
      </div>
      {longest > 0 && (
        <div className="streak-best">
          Récord: {longest} días
        </div>
      )}
    </div>
  )
}