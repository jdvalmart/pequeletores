import { iconCategories } from '../data/icons'
import { allIcons } from '../data/icons'
import './IconPicker.css'

interface IconPickerProps {
  selectedIcons: string[]
  onChange: (icons: string[]) => void
  maxSelection?: number
}

export function IconPicker({ selectedIcons, onChange, maxSelection = 5 }: IconPickerProps) {
  const handleIconClick = (iconId: string) => {
    if (selectedIcons.includes(iconId)) {
      onChange(selectedIcons.filter(id => id !== iconId))
    } else if (selectedIcons.length < maxSelection) {
      onChange([...selectedIcons, iconId])
    }
  }

  return (
    <div className="icon-picker">
      <p className="icon-picker-hint">
        ¡Selecciona hasta {maxSelection} cosas que te gusten (toca para elegir)!
      </p>
      
      {Object.entries(iconCategories).map(([category, data]) => (
        <div key={category} className="icon-category">
          <h3 className="category-label">{data.label}</h3>
          <div className="icon-grid">
            {data.icons.map(icon => (
              <button
                key={icon.id}
                type="button"
                className={`icon-button ${selectedIcons.includes(icon.id) ? 'selected' : ''}`}
                onClick={() => handleIconClick(icon.id)}
                disabled={!selectedIcons.includes(icon.id) && selectedIcons.length >= maxSelection}
                title={icon.label}
              >
                <span className="icon-emoji">{icon.emoji}</span>
                <span className="icon-label">{icon.label}</span>
                {selectedIcons.includes(icon.id) && (
                  <span className="check-mark">✓</span>
                )}
              </button>
            ))}
          </div>
        </div>
      ))}
      
      {selectedIcons.length > 0 && (
        <div className="selected-summary">
          <p>¡Seleccionaste:</p>
          <div className="selected-icons">
            {selectedIcons.map(id => {
              const icon = allIcons.find(i => i.id === id)
              return (
                <span key={id} className="selected-icon" onClick={() => handleIconClick(id)}>
                  {icon?.emoji} {icon?.label}
                </span>
              )
            })}
          </div>
        </div>
      )}
    </div>
  )
}