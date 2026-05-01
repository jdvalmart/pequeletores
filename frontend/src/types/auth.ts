/**
 * Authentication types for PequeLectores
 */

// Token response from the API
export interface TokenResponse {
  access_token: string;
  token_type: 'bearer';
}

// Parent user data
export interface Parent {
  id: number;
  email: string;
}

// Child profile
export interface Child {
  id: number;
  name: string;
  birth_date: string; // ISO date string
  age: number;
  parent_id: number | null;
}

// Login request
export interface LoginRequest {
  email: string;
  password: string;
}

// Register request
export interface RegisterRequest {
  email: string;
  password: string;
}

// Auth state
export interface AuthState {
  isAuthenticated: boolean;
  parent: Parent | null;
  token: string | null;
}

// Stored auth data
export interface StoredAuth {
  token: string;
  parent: Parent;
  expiresAt: number;
}

// API error response
export interface ApiError {
  detail: string;
  errors?: Array<{
    field: string;
    message: string;
    type: string;
  }>;
}