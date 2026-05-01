/**
 * API Client for PequeLectores
 * With strict types and proper error handling
 */

import axios, { AxiosError, AxiosResponse, InternalAxiosRequestConfig } from 'axios';
import type { TokenResponse, Parent, ApiError } from '../types/auth';
import type { BookData, PreferencesData, ReadingLogData } from '../schemas/common';

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

/**
 * Custom API Error with typed response
 */
export class ApiClientError<T = unknown> extends Error {
  status: number;
  data: T | null;
  isNetworkError: boolean;
  isValidationError: boolean;

  constructor(message: string, status: number, data: T | null = null) {
    super(message);
    this.name = 'ApiClientError';
    this.status = status;
    this.data = data;
    this.isNetworkError = status === 0;
    this.isValidationError = status === 422;
  }
}

// Request interceptor for logging and auth
apiClient.interceptors.request.use(
  (config: InternalAxiosRequestConfig) => {
    // Log request in development
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

// Response interceptor with error handling
apiClient.interceptors.response.use(
  (response: AxiosResponse) => {
    return response;
  },
  (error: AxiosError<ApiError>) => {
    if (import.meta.env.DEV) {
      console.error('[API] Response error:', error.response?.data);
    }

    if (!error.response) {
      // Network error
      throw new ApiClientError(
        'Network error. Please check your connection.',
        0
      );
    }

    const status = error.response.status;
    const data = error.response.data;

    // Handle specific error codes
    switch (status) {
      case 401:
        throw new ApiClientError('Unauthorized. Please log in again.', status, data);
      case 403:
        throw new ApiClientError('Access denied.', status, data);
      case 404:
        throw new ApiClientError('Resource not found.', status, data);
      case 409:
        throw new ApiClientError(data.detail || 'Conflict.', status, data);
      case 422:
        throw new ApiClientError(
          data.detail || 'Validation error.',
          status,
          data
        );
      case 500:
        throw new ApiClientError('Server error. Please try again later.', status, data);
      default:
        throw new ApiClientError(
          data?.detail || 'An unexpected error occurred.',
          status,
          data
        );
    }
  }
);

// ============================================
// Auth API
// ============================================

export async function register(email: string, password: string): Promise<TokenResponse> {
  const response = await apiClient.post<TokenResponse>('/api/auth/register', {
    email,
    password
  });
  return response.data;
}

export async function login(email: string, password: string): Promise<TokenResponse> {
  const response = await apiClient.post<TokenResponse>('/api/auth/login', {
    email,
    password
  });
  return response.data;
}

export async function getCurrentParent(token: string): Promise<Parent> {
  const response = await apiClient.get<Parent>('/api/auth/me', {
    headers: { Authorization: `Bearer ${token}` }
  });
  return response.data;
}

// ============================================
// Preferences API
// ============================================

export async function savePreferences(
  childId: number,
  iconIds: string[],
  token?: string
): Promise<PreferencesData> {
  const response = await apiClient.post<PreferencesData>('/api/preferences', {
    child_id: childId,
    icon_ids: iconIds
  }, token ? authHeaders(token) : undefined);
  return response.data;
}

export async function getPreferences(
  childId: number,
  token?: string
): Promise<PreferencesData> {
  const response = await apiClient.get<PreferencesData>(`/api/preferences/${childId}`, 
    token ? { headers: authHeaders(token) } : undefined
  );
  return response.data;
}

// ============================================
// Recommendations API
// ============================================

export async function getRecommendations(
  childId: number,
  limit = 10,
  token?: string
): Promise<BookData[]> {
  const response = await apiClient.get<BookData[]>('/api/recommendations', {
    params: { child_id: childId, limit },
    ...(token ? { headers: authHeaders(token) } : {})
  });
  return response.data;
}

// ============================================
// Reading API
// ============================================

export async function logReading(
  childId: number,
  bookId: string,
  pagesRead: number,
  token?: string
): Promise<ReadingLogData> {
  const response = await apiClient.post<ReadingLogData>('/api/reading/log', {
    child_id: childId,
    book_id: bookId,
    pages_read: pagesRead
  }, token ? { headers: authHeaders(token) } : {});
  return response.data;
}

export async function getStreak(childId: number, token?: string): Promise<{ streak: number }> {
  const response = await apiClient.get<{ streak: number }>(`/api/reading/streak/${childId}`,
    token ? { headers: authHeaders(token) } : {}
  );
  return response.data;
}

// ============================================
// Badges API
// ============================================

export async function getAllBadges(token?: string): Promise<Badge[]> {
  const response = await apiClient.get<Badge[]>('/api/badges',
    token ? { headers: authHeaders(token) } : {}
  );
  return response.data;
}

export async function getChildBadges(childId: number, token?: string): Promise<Badge[]> {
  const response = await apiClient.get<Badge[]>(`/api/badges/${childId}`,
    token ? { headers: authHeaders(token) } : {}
  );
  return response.data;
}

export async function checkBadges(childId: number, token?: string): Promise<{ new_badges: Badge[] }> {
  const response = await apiClient.post<{ new_badges: Badge[] }>(`/api/badges/${childId}/check`, {},
    token ? { headers: authHeaders(token) } : {}
  );
  return response.data;
}

// ============================================
// Helpers
// ============================================

function authHeaders(token: string): { headers: { Authorization: string } } {
  return { headers: { Authorization: `Bearer ${token}` } };
}

/**
 * Parse child ID from string or number
 */
export function parseChildId(childId: string | number): number {
  const parsed = typeof childId === 'string' ? parseInt(childId, 10) : childId;
  return isNaN(parsed) ? 1 : parsed;
}

// Type for Badge
interface Badge {
  id: number;
  name: string;
  description: string;
  icon: string;
  requirement: number;
}

export { apiClient };
export type { Badge };