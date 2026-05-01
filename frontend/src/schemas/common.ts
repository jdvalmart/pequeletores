/**
 * Common Zod schemas
 */

import { z } from 'zod';

// Valid icon IDs (from frontend icons.ts)
export const VALID_ICON_IDS = [
  'dinosaur', 'dragon', 'dog', 'cat', 'horse', 'butterfly',
  'rocket', 'compass', 'mountain', 'ship', 'treasure', 'map',
  'wizard', 'fairy', 'ghost', 'magic', 'castle', 'crown',
  'science', 'earth', 'star', 'robot', 'brain', 'lightbulb',
  'soccer', 'basketball', 'swimming', 'bicycle', 'trophy', 'medal',
  'laugh', 'art', 'music', 'game', 'camera', 'heart'
] as const;

// Preferences schema
export const preferencesSchema = z.object({
  child_id: z.number().positive('Child ID must be positive'),
  icon_ids: z.array(z.string()).min(1, 'At least one icon is required').max(10, 'Maximum 10 icons allowed'),
});

// Validate icon IDs
preferencesSchema.refine(
  (data) => data.icon_ids.every((id) => VALID_ICON_IDS.includes(id as typeof VALID_ICON_IDS[number])),
  {
    message: 'Invalid icon ID',
    path: ['icon_ids'],
  }
);

// Book schema (from Open Library)
export const bookSchema = z.object({
  key: z.string(),
  title: z.string(),
  author: z.array(z.string()).optional(),
  subjects: z.array(z.string()).optional(),
  cover_url: z.string().nullable().optional(),
  first_publish_year: z.number().optional(),
  score: z.number().optional(),
});

// Reading log schema
export const readingLogSchema = z.object({
  child_id: z.number().positive(),
  book_id: z.string().min(1, 'Book ID is required'),
  pages_read: z.number().positive('Pages must be positive'),
});

// Type inference
export type PreferencesData = z.infer<typeof preferencesSchema>;
export type BookData = z.infer<typeof bookSchema>;
export type ReadingLogData = z.infer<typeof readingLogSchema>;
export type IconId = typeof VALID_ICON_IDS[number];

// Validation helpers
export function validatePreferences(data: unknown): { success: true; data: PreferencesData } | { success: false; errors: string[] } {
  const result = preferencesSchema.safeParse(data);
  
  if (result.success) {
    return { success: true, data: result.data };
  }
  
  const errors = result.error.errors.map((e) => e.message);
  return { success: false, errors };
}