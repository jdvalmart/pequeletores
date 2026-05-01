export interface Child {
  id: string
  name: string
  birth_date: string
  age: number
}

export const childSchema = {
  id: { type: 'string' as const, required: true },
  name: { type: 'string' as const, required: true },
  birth_date: { type: 'string' as const, required: true },
  age: { type: 'number' as const, required: true }
}