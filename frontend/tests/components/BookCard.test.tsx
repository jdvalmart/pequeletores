/**
 * Tests for BookCard component
 */

import { describe, it, expect, vi } from 'vitest';
import { render, screen, fireEvent } from '@testing-library/react';
import { BookCard, BookGrid } from '../../src/components/BookCard';
import type { BookWithScore } from '../../src/types';

describe('BookCard', () => {
  const mockBook: BookWithScore = {
    key: '/works/OL123W',
    title: 'Harry Potter and the Sorcerer\'s Stone',
    author: ['J.K. Rowling'],
    subjects: ['fantasy', 'magic'],
    cover_url: null,
    first_publish_year: 1997,
    score: 0.95
  };

  it('should render book title', () => {
    render(<BookCard book={mockBook} />);
    
    expect(screen.getByText('Harry Potter and the Sorcerer\'s Stone')).toBeInTheDocument();
  });

  it('should render author', () => {
    render(<BookCard book={mockBook} />);
    
    expect(screen.getByText('J.K. Rowling')).toBeInTheDocument();
  });

  it('should render publication year', () => {
    render(<BookCard book={mockBook} />);
    
    expect(screen.getByText('1997')).toBeInTheDocument();
  });

  it('should render score as percentage', () => {
    render(<BookCard book={mockBook} />);
    
    expect(screen.getByText('95%')).toBeInTheDocument();
  });

  it('should show button when onLogReading is provided', () => {
    const onLogReading = vi.fn();
    render(<BookCard book={mockBook} onLogReading={onLogReading} />);
    
    const button = screen.getByText('I read this! 📖');
    expect(button).toBeInTheDocument();
  });

  it('should call onLogReading when button is clicked', () => {
    const onLogReading = vi.fn();
    render(<BookCard book={mockBook} onLogReading={onLogReading} />);
    
    fireEvent.click(screen.getByText('I read this! 📖'));
    
    expect(onLogReading).toHaveBeenCalledWith(10);
  });

  it('should not show button when onLogReading is not provided', () => {
    render(<BookCard book={mockBook} />);
    
    expect(screen.queryByText('I read this! 📖')).not.toBeInTheDocument();
  });

  it('should handle missing author', () => {
    const bookWithoutAuthor: BookWithScore = {
      key: '/works/OL123W',
      title: 'Unknown Book',
      score: 0.5
    };
    
    render(<BookCard book={bookWithoutAuthor} />);
    
    expect(screen.getByText('Unknown Author')).toBeInTheDocument();
  });
});

describe('BookGrid', () => {
  const mockBooks: BookWithScore[] = [
    {
      key: '/works/OL1',
      title: 'Book One',
      author: ['Author One'],
      score: 0.9
    },
    {
      key: '/works/OL2',
      title: 'Book Two',
      author: ['Author Two'],
      score: 0.8
    }
  ];

  it('should render all books', () => {
    render(<BookGrid books={mockBooks} />);
    
    expect(screen.getByText('Book One')).toBeInTheDocument();
    expect(screen.getByText('Book Two')).toBeInTheDocument();
  });

  it('should render empty message when no books', () => {
    render(<BookGrid books={[]} />);
    
    expect(screen.getByText('No books found. Try adjusting your preferences!')).toBeInTheDocument();
  });

  it('should pass onLogReading to BookCard', () => {
    const onLogReading = vi.fn();
    render(<BookGrid books={mockBooks} onLogReading={onLogReading} />);
    
    fireEvent.click(screen.getAllByText('I read this! 📖')[0]);
    
    expect(onLogReading).toHaveBeenCalledWith('/works/OL1', 10);
  });
});