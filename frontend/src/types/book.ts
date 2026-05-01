export interface Book {
  key: string
  title: string
  author: string[]
  cover_url: string | null
  subjects: string[]
  first_publish_year: number | null
}

export interface BookWithScore extends Book {
  score: number
}

export const bookSchema = {
  key: { type: 'string' as const, required: true },
  title: { type: 'string' as const, required: true },
  author: { type: 'array' as const, required: false },
  cover_url: { type: 'string' as const, required: false },
  subjects: { type: 'array' as const, required: false },
  first_publish_year: { type: 'number' as const, required: false }
}

export const bookResponseSchema = {
  books: { type: 'array' as const, itemSchema: bookSchema },
  total: { type: 'number' as const, required: true }
}