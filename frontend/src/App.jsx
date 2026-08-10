import React from 'react';
import { ThemeProvider } from './context/ThemeContext';
import { AuthProvider, useAuth } from './context/AuthContext';
import LandingPage from './components/landing/LandingPage';
import AuthPage from './components/auth/AuthPage';
import ClaudeWorkspace from './components/app/ClaudeWorkspace';

function AppContent() {
  const { activeView } = useAuth();

  switch (activeView) {
    case 'auth':
      return <AuthPage />;
    case 'app':
      return <ClaudeWorkspace />;
    case 'landing':
    default:
      return <LandingPage />;
  }
}

export default function App() {
  return (
    <ThemeProvider>
      <AuthProvider>
        <AppContent />
      </AuthProvider>
    </ThemeProvider>
  );
}
