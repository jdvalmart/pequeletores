/**
 * Tests for Home page
 */

import { describe, it, expect } from 'vitest';
import { render, screen } from '@testing-library/react';
import { BrowserRouter } from 'react-router-dom';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { HomePage } from '../../src/pages/Home';

// Wrapper with QueryClient and Router
const TestWrapper = ({ children }: { children: React.ReactNode }) => {
  const queryClient = new QueryClient({
    defaultOptions: {
      queries: { retry: false },
    },
  });

  return (
    <QueryClientProvider client={queryClient}>
      <BrowserRouter>
        {children}
      </BrowserRouter>
    </QueryClientProvider>
  );
};

// Render with all providers
const renderWithProviders = (component: React.ReactElement) => {
  return render(
    <TestWrapper>
      {component}
    </TestWrapper>
  );
};

describe('HomePage', () => {
  it('should render app title', () => {
    renderWithProviders(<HomePage />);
    
    expect(screen.getByText('📚 PequeLectores')).toBeInTheDocument();
  });

  it('should render tagline', () => {
    renderWithProviders(<HomePage />);
    
    expect(screen.getByText('¡Descubre tu próxima aventura literaria!')).toBeInTheDocument();
  });

  it('should render navigation cards', () => {
    renderWithProviders(<HomePage />);
    
    expect(screen.getByText('Elige tus Intereses')).toBeInTheDocument();
    expect(screen.getByText('Ver Recomendaciones')).toBeInTheDocument();
    expect(screen.getByText('Mi Perfil')).toBeInTheDocument();
  });

  it('should render tip section', () => {
    renderWithProviders(<HomePage />);
    
    expect(screen.getByText(/Consejo:/)).toBeInTheDocument();
  });

  it('should have correct navigation links', () => {
    renderWithProviders(<HomePage />);
    
    const preferencesLink = screen.getByText('Elige tus Intereses').closest('a');
    const recommendationsLink = screen.getByText('Ver Recomendaciones').closest('a');
    const profileLink = screen.getByText('Mi Perfil').closest('a');
    
    expect(preferencesLink).toHaveAttribute('href', '/preferences');
    expect(recommendationsLink).toHaveAttribute('href', '/recommendations');
    expect(profileLink).toHaveAttribute('href', '/profile');
  });

  it('should render icons for navigation cards', () => {
    renderWithProviders(<HomePage />);
    
    // Check for emoji icons
    expect(screen.getByText('🎨')).toBeInTheDocument();
    expect(screen.getByText('📖')).toBeInTheDocument();
    expect(screen.getByText('👤')).toBeInTheDocument();
  });

  it('should render streak section', () => {
    renderWithProviders(<HomePage />);
    
    // The StreakCounter should be rendered (shows loading state)
    const streakSection = document.querySelector('.streak-section');
    expect(streakSection).toBeInTheDocument();
  });

  it('should render all navigation cards with proper classes', () => {
    renderWithProviders(<HomePage />);
    
    expect(document.querySelector('.nav-card.choose-books')).toBeInTheDocument();
    expect(document.querySelector('.nav-card.get-recommendations')).toBeInTheDocument();
    expect(document.querySelector('.nav-card.my-profile')).toBeInTheDocument();
  });
});