// Book types
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

// Child types
export interface Child {
  id: string
  name: string
  birth_date: string
  age: number
}