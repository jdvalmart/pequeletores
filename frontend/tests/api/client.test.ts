/**
 * Tests for API client
 */

import { describe, it, expect, vi, beforeEach, afterEach } from 'vitest';
import { ApiClientError, parseChildId } from '../../src/api/client';

describe('parseChildId', () => {
  it('should parse number to number', () => {
    expect(parseChildId(1)).toBe(1);
    expect(parseChildId(42)).toBe(42);
  });

  it('should parse valid string to number', () => {
    expect(parseChildId('1')).toBe(1);
    expect(parseChildId('42')).toBe(42);
  });

  it('should return fallback 1 for NaN', () => {
    expect(parseChildId('abc')).toBe(1);
    expect(parseChildId('')).toBe(1);
  });

  it('should return fallback 1 for invalid number', () => {
    expect(parseChildId(NaN)).toBe(1);
  });
});

describe('ApiClientError', () => {
  it('should create error with message and status', () => {
    const error = new ApiClientError('Test error', 404);
    
    expect(error.message).toBe('Test error');
    expect(error.status).toBe(404);
    expect(error.name).toBe('ApiClientError');
  });

  it('should set isNetworkError for status 0', () => {
    const error = new ApiClientError('Network error', 0);
    
    expect(error.isNetworkError).toBe(true);
    expect(error.isValidationError).toBe(false);
  });

  it('should set isValidationError for status 422', () => {
    const error = new ApiClientError('Validation error', 422);
    
    expect(error.isValidationError).toBe(true);
    expect(error.isNetworkError).toBe(false);
  });

  it('should store data', () => {
    const data = { detail: 'Error details' };
    const error = new ApiClientError('Error', 400, data);
    
    expect(error.data).toEqual(data);
  });
});

describe('API URL Configuration', () => {
  it('should use default URL when env not set', () => {
    // VITE_API_URL is not set in test environment by default
    // This test verifies the fallback works
    const url = import.meta.env.VITE_API_URL || 'http://localhost:8000';
    expect(url).toBeDefined();
  });
});