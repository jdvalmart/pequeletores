import type { BookWithScore } from '../types'
import './BookCard.css'

interface BookCardProps {
  book: BookWithScore
  onLogReading?: (pages: number) => void
}

export function BookCard({ book, onLogReading }: BookCardProps) {
  const coverUrl = book.cover_url || `https://covers.openlibrary.org/b/isbn/${book.key}-M.jpg`
  
  return (
    <div className="book-card">
      <div className="book-cover">
        <img 
          src={coverUrl} 
          alt={book.title}
          onError={(e) => {
            (e.target as HTMLImageElement).src = 'https://covers.openlibrary.org/b/isbn/9780140328721-M.jpg'
          }}
        />
      </div>
      <div className="book-info">
        <h3 className="book-title">{book.title}</h3>
        <p className="book-author">{Array.isArray(book.author) ? book.author.join(', ') : book.author || 'Unknown Author'}</p>
        {book.first_publish_year && (
          <p className="book-year">{book.first_publish_year}</p>
        )}
        {book.score !== undefined && (
          <div className="book-score">
            <span className="score-label">Match:</span>
            <span className="score-value">{Math.round(book.score * 100)}%</span>
          </div>
        )}
        {onLogReading && (
          <button 
            className="log-reading-btn"
            onClick={() => onLogReading(10)}
          >
            I read this! 📖
          </button>
        )}
      </div>
    </div>
  )
}

interface BookGridProps {
  books: BookWithScore[]
  onLogReading?: (bookKey: string, pages: number) => void
}

export function BookGrid({ books, onLogReading }: BookGridProps) {
  if (books.length === 0) {
    return (
      <div className="book-grid-empty">
        <p>No books found. Try adjusting your preferences!</p>
      </div>
    )
  }
  
  return (
    <div className="book-grid">
      {books.map(book => (
        <BookCard 
          key={book.key} 
          book={book}
          onLogReading={onLogReading ? () => onLogReading(book.key, 10) : undefined}
        />
      ))}
    </div>
  )
}