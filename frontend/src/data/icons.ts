// Icon categories for preference selection
export const iconCategories = {
  animals: {
    label: '🐾 Animales',
    icons: [
      { id: 'dog', emoji: '🐕', label: 'Perros' },
      { id: 'cat', emoji: '🐱', label: 'Gatos' },
      { id: 'dinosaur', emoji: '🦖', label: 'Dinosaurios' },
      { id: 'horse', emoji: '🦄', label: 'Unicornios' },
      { id: 'dragon', emoji: '🐉', label: 'Dragones' },
      { id: 'butterfly', emoji: '🦋', label: 'Mariposas' }
    ]
  },
  adventure: {
    label: '🗺️ Aventura',
    icons: [
      { id: 'rocket', emoji: '🚀', label: 'Espacio' },
      { id: 'compass', emoji: '🧭', label: 'Exploradores' },
      { id: 'mountain', emoji: '⛰️', label: 'Montañas' },
      { id: 'ship', emoji: '⛵', label: 'Barcos' },
      { id: 'treasure', emoji: '💎', label: 'Tesoros' },
      { id: 'map', emoji: '🗺️', label: 'Mapas' }
    ]
  },
  fantasy: {
    label: '✨ Fantasía',
    icons: [
      { id: 'wizard', emoji: '🧙', label: 'Magos' },
      { id: 'fairy', emoji: '🧚', label: 'Hadas' },
      { id: 'ghost', emoji: '👻', label: 'Fantasmas' },
      { id: 'magic', emoji: '✨', label: 'Magia' },
      { id: 'castle', emoji: '🏰', label: 'Castillos' },
      { id: 'crown', emoji: '👑', label: 'Coronas' }
    ]
  },
  science: {
    label: '🔬 Ciencia',
    icons: [
      { id: 'science', emoji: '🔬', label: 'Ciencia' },
      { id: 'earth', emoji: '🌍', label: 'Tierra' },
      { id: 'star', emoji: '⭐', label: 'Estrellas' },
      { id: 'robot', emoji: '🤖', label: 'Robots' },
      { id: 'brain', emoji: '🧠', label: 'Cerebro' },
      { id: 'lightbulb', emoji: '💡', label: 'Ideas' }
    ]
  },
  sports: {
    label: '⚽ Deportes',
    icons: [
      { id: 'soccer', emoji: '⚽', label: 'Fútbol' },
      { id: 'basketball', emoji: '🏀', label: 'Baloncesto' },
      { id: 'swimming', emoji: '🏊', label: 'Natación' },
      { id: 'bicycle', emoji: '🚴', label: 'Ciclismo' },
      { id: 'trophy', emoji: '🏆', label: 'Trofeos' },
      { id: 'medal', emoji: '🥇', label: 'Medallas' }
    ]
  },
  fun: {
    label: '🎉 Diversión',
    icons: [
      { id: 'laugh', emoji: '😂', label: 'Divertido' },
      { id: 'art', emoji: '🎨', label: 'Arte' },
      { id: 'music', emoji: '🎵', label: 'Música' },
      { id: 'game', emoji: '🎮', label: 'Videojuegos' },
      { id: 'camera', emoji: '📷', label: 'Fotos' },
      { id: 'heart', emoji: '❤️', label: 'Amor' }
    ]
  }
}

export type IconId = keyof typeof iconCategories

export const allIcons = Object.entries(iconCategories).flatMap(([category, data]) =>
  data.icons.map(icon => ({ ...icon, category }))
)