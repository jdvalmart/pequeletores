/**
 * API Client for PequeLectores
 */

import axios, { AxiosError, AxiosResponse, InternalAxiosRequestConfig } from 'axios';
import type { TokenResponse, Parent, ApiError } from '../types/auth';

// API Configuration
const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';
const TIMEOUT = 10000;

// Create axios instance
const apiClient = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json'
  },
  timeout: TIMEOUT
});

// ============================================
// Error Handling
// ============================================

export class ApiClientError<T = unknown> extends Error {
  status: number;
  data: T | null;
  isNetworkError: boolean;

  constructor(message: string, status: number, data: T | null = null) {
    super(message);
    this.name = 'ApiClientError';
    this.status = status;
    this.data = data;
    this.isNetworkError = status === 0;
  }
}

// Request interceptor
apiClient.interceptors.request.use(
  (config: InternalAxiosRequestConfig) => {
    if (import.meta.env.DEV) {
      console.log(`[API] ${config.method?.toUpperCase()} ${config.url}`);
    }
    return config;
  },
  (error) => {
    console.error('[API] Request error:', error);
    return Promise.reject(error);
  }
);

// Response interceptor
apiClient.interceptors.response.use(
  (response: AxiosResponse) => response,
  (error: AxiosError<ApiError>) => {
    if (import.meta.env.DEV) {
      console.error('[API] Response error:', error.response?.data);
    }

    if (!error.response) {
      throw new ApiClientError('Network error. Please check your connection.', 0);
    }

    const status = error.response.status;
    const data = error.response.data;

    switch (status) {
      case 401:
        throw new ApiClientError('Unauthorized. Please log in again.', status, data);
      case 403:
        throw new ApiClientError('Access denied.', status, data);
      case 404:
        throw new ApiClientError('Resource not found.', status, data);
      case 422:
        throw new ApiClientError(data?.detail || 'Validation error.', status, data);
      case 500:
        throw new ApiClientError('Server error. Please try again later.', status, data);
      default:
        throw new ApiClientError(data?.detail || 'An unexpected error occurred.', status, data);
    }
  }
);

// ============================================
// Auth API
// ============================================

export async function register(email: string, password: string): Promise<TokenResponse> {
  const response = await apiClient.post<TokenResponse>('/api/auth/register', { email, password });
  return response.data;
}

export async function login(email: string, password: string): Promise<TokenResponse> {
  const response = await apiClient.post<TokenResponse>('/api/auth/login', { email, password });
  return response.data;
}

export async function getCurrentParent(token: string): Promise<Parent> {
  const response = await apiClient.get<Parent>('/api/auth/me', {
    headers: { Authorization: `Bearer ${token}` }
  });
  return response.data;
}

// ============================================
// Helpers
// ============================================

function getAuthConfig(token?: string) {
  return token ? { headers: { Authorization: `Bearer ${token}` } } : undefined;
}

// ============================================
// Preferences API
// ============================================

export interface PreferencesData {
  id: number;
  child_id: number;
  icon_ids: string[];
  created_at: string;
  updated_at: string;
}

export async function savePreferences(
  childId: number,
  iconIds: string[],
  token?: string
): Promise<PreferencesData> {
  const response = await apiClient.post<PreferencesData>(
    '/api/preferences',
    { child_id: childId, icon_ids: iconIds },
    getAuthConfig(token)
  );
  return response.data;
}

export async function getPreferences(
  childId: number,
  token?: string
): Promise<PreferencesData> {
  const response = await apiClient.get<PreferencesData>(
    `/api/preferences/${childId}`,
    getAuthConfig(token)
  );
  return response.data;
}

// ============================================
// Recommendations API
// ============================================

export interface BookData {
  key: string;
  title: string;
  author?: string;
  cover_url?: string | null;
  first_publish_year?: number | null;
  subject?: string[];
  score?: number;
}

export interface BookWithScore {
  key: string;
  title: string;
  author: string[];
  cover_url: string | null;
  subjects: string[];
  first_publish_year: number | null;
  score: number;
}

export interface RecommendationsResponse {
  recommendations: BookData[];
  total: number;
}

export async function getRecommendations(
  childId: number,
  limit = 10,
  token?: string
): Promise<RecommendationsResponse> {
  const response = await apiClient.get<RecommendationsResponse>('/api/recommendations', {
    params: { child_id: childId, limit },
    ...getAuthConfig(token)
  });
  return response.data;
}

// ============================================
// Reading API
// ============================================

export interface ReadingLogData {
  id: number;
  child_id: number;
  book_id: string;
  pages_read: number;
  logged_at: string;
}

export interface StreakData {
  streak: number;
  current_streak: number;
  longest_streak: number;
  total_books: number;
  total_pages: number;
}

export async function logReading(
  childId: number,
  bookId: string,
  pagesRead: number,
  token?: string
): Promise<ReadingLogData> {
  const response = await apiClient.post<ReadingLogData>(
    '/api/reading/log',
    { child_id: childId, book_id: bookId, pages_read: pagesRead },
    getAuthConfig(token)
  );
  return response.data;
}

export async function getStreak(childId: number, token?: string): Promise<StreakData> {
  const response = await apiClient.get<StreakData>(
    `/api/reading/streak/${childId}`,
    getAuthConfig(token)
  );
  return response.data;
}

// ============================================
// Badges API
// ============================================

export interface Badge {
  id: number;
  name: string;
  description: string;
  icon: string;
  requirement: number;
}

export interface ChildBadgesResponse {
  earned: Badge[];
  unearned: Badge[];
  total_earned: number;
}

export async function getAllBadges(token?: string): Promise<Badge[]> {
  const response = await apiClient.get<Badge[]>('/api/badges', getAuthConfig(token));
  return response.data;
}

export async function getChildBadges(childId: number, token?: string): Promise<ChildBadgesResponse> {
  const response = await apiClient.get<ChildBadgesResponse>(
    `/api/badges/${childId}`,
    getAuthConfig(token)
  );
  return response.data;
}

export async function checkBadges(childId: number, token?: string): Promise<{ new_badges: Badge[] }> {
  const response = await apiClient.post<{ new_badges: Badge[] }>(
    `/api/badges/${childId}/check`,
    {},
    getAuthConfig(token)
  );
  return response.data;
}

// ============================================
// Helpers
// ============================================

export function parseChildId(childId: string | number): number {
  const parsed = typeof childId === 'string' ? parseInt(childId, 10) : childId;
  return isNaN(parsed) ? 1 : parsed;
}

export { apiClient };