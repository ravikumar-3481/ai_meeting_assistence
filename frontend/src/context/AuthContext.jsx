import React, { createContext, useContext, useState, useEffect } from 'react';
import { api } from '../services/api';

const AuthContext = createContext({
  isAuthenticated: false,
  user: null,
  activeView: 'landing', // 'landing', 'auth', 'app'
  authTab: 'login', // 'login', 'signup', 'forgot_password'
  error: null,
  loading: false,
  navigateTo: () => {},
  login: async () => {},
  signup: async () => {},
  resetPassword: async () => {},
  demoLogin: async () => {},
  logout: async () => {},
  setAuthTab: () => {},
  setError: () => {},
});

export function AuthProvider({ children }) {
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [user, setUser] = useState(() => {
    const saved = localStorage.getItem('meeting_sense_user');
    return saved ? JSON.parse(saved) : null;
  });
  const [activeView, setActiveView] = useState(() => {
    return localStorage.getItem('meeting_sense_token') ? 'app' : 'landing';
  });
  const [authTab, setAuthTab] = useState('login');
  const [error, setError] = useState(null);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    const token = localStorage.getItem('meeting_sense_token');
    if (token) {
      setIsAuthenticated(true);
      api.getProfile()
        .then((res) => {
          if (res.data) {
            const userData = {
              id: res.data.id || res.data.user_id,
              name: res.data.full_name || res.data.email?.split('@')[0] || 'User',
              email: res.data.email,
              role: res.data.role || 'Member',
            };
            setUser(userData);
            localStorage.setItem('meeting_sense_user', JSON.stringify(userData));
          }
        })
        .catch((err) => {
          console.warn('Could not verify profile from Supabase DB:', err);
        });
    }
  }, []);

  const navigateTo = (view, tab = 'login') => {
    setActiveView(view);
    if (tab) setAuthTab(tab);
    setError(null);
  };

  const login = async (email, password) => {
    setLoading(true);
    setError(null);
    try {
      const response = await api.login(email, password);
      const data = response.data;
      if (data && data.access_token) {
        localStorage.setItem('meeting_sense_token', data.access_token);
        const userData = {
          id: data.user_id,
          email: data.email,
          name: data.email.split('@')[0],
          role: 'Team Member',
        };
        setUser(userData);
        localStorage.setItem('meeting_sense_user', JSON.stringify(userData));
        setIsAuthenticated(true);
        setActiveView('app');
        return { success: true };
      }
      throw new Error(response.message || 'Login failed.');
    } catch (err) {
      console.error('Supabase Login Error:', err);
      setError(err.message || 'Invalid email or password.');
      return { success: false, error: err.message };
    } finally {
      setLoading(false);
    }
  };

  const signup = async (name, email, password, role) => {
    setLoading(true);
    setError(null);
    try {
      const response = await api.register(email, password, name);
      const data = response.data;
      if (data && data.access_token) {
        localStorage.setItem('meeting_sense_token', data.access_token);
        const userData = {
          id: data.user_id,
          email: data.email,
          name: name || data.email.split('@')[0],
          role: role || 'Member',
        };
        setUser(userData);
        localStorage.setItem('meeting_sense_user', JSON.stringify(userData));
        setIsAuthenticated(true);
        setActiveView('app');
        return { success: true };
      }
      throw new Error(response.message || 'Signup failed.');
    } catch (err) {
      console.error('Supabase Signup Error:', err);
      setError(err.message || 'Registration failed. Check email or password requirements.');
      return { success: false, error: err.message };
    } finally {
      setLoading(false);
    }
  };

  const resetPassword = async (email) => {
    setLoading(true);
    setError(null);
    try {
      const response = await api.resetPassword(email);
      return { success: true, message: response.message || 'Password reset email sent successfully!' };
    } catch (err) {
      console.error('Supabase Reset Password Error:', err);
      setError(err.message || 'Failed to send password reset email.');
      return { success: false, error: err.message };
    } finally {
      setLoading(false);
    }
  };

  const demoLogin = async () => {
    // Standard workspace access
    localStorage.setItem('meeting_sense_token', 'demo_access_token');
    const demoUser = {
      id: '930c2fca-3151-4094-a409-91d55e26cac4',
      email: 'ravivish517@gmail.com',
      name: 'Ravi Kumar',
      role: 'Product Lead',
    };
    setUser(demoUser);
    localStorage.setItem('meeting_sense_user', JSON.stringify(demoUser));
    setIsAuthenticated(true);
    setActiveView('app');
  };

  const logout = async () => {
    await api.logout();
    setUser(null);
    setIsAuthenticated(false);
    setActiveView('landing');
  };

  return (
    <AuthContext.Provider
      value={{
        isAuthenticated,
        user,
        activeView,
        authTab,
        error,
        loading,
        navigateTo,
        login,
        signup,
        resetPassword,
        demoLogin,
        logout,
        setAuthTab,
        setError,
      }}
    >
      {children}
    </AuthContext.Provider>
  );
}

export function useAuth() {
  return useContext(AuthContext);
}
