import React, { useState } from 'react';
import { useAuth } from '../../context/AuthContext';
import ThemeToggle from './ThemeToggle';
import { Sparkles, Menu, X, ArrowRight, Bot } from 'lucide-react';
import { motion, AnimatePresence } from 'framer-motion';

export default function Navbar() {
  const { isAuthenticated, activeView, navigateTo, demoLogin } = useAuth();
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);

  const handleNavClick = (sectionId) => {
    setMobileMenuOpen(false);
    if (activeView !== 'landing') {
      navigateTo('landing');
      setTimeout(() => {
        const el = document.getElementById(sectionId);
        if (el) el.scrollIntoView({ behavior: 'smooth' });
      }, 100);
    } else {
      const el = document.getElementById(sectionId);
      if (el) el.scrollIntoView({ behavior: 'smooth' });
    }
  };

  return (
    <header className="sticky top-0 z-50 backdrop-blur-xl bg-zinc-950/80 dark:bg-zinc-950/90 light:bg-white/90 border-b border-zinc-800/60 dark:border-zinc-800/80 light:border-zinc-200 transition-colors">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex items-center justify-between h-16 sm:h-20">
          
          {/* Brand Logo */}
          <div 
            onClick={() => navigateTo('landing')}
            className="flex items-center gap-3 cursor-pointer group"
          >
            <div className="w-10 h-10 rounded-xl bg-gradient-to-br from-indigo-500 via-purple-500 to-emerald-500 p-[1.5px] shadow-lg shadow-indigo-500/20 group-hover:scale-105 transition-transform duration-200">
              <div className="w-full h-full bg-zinc-950 rounded-[10.5px] flex items-center justify-center">
                <Bot className="w-5 h-5 text-indigo-400 group-hover:text-emerald-400 transition-colors" />
              </div>
            </div>
            <div className="flex flex-col">
              <span className="font-bold text-lg tracking-tight text-zinc-100 dark:text-zinc-100 light:text-zinc-900 group-hover:text-indigo-400 transition-colors flex items-center gap-1.5">
                MeetingSense <span className="text-xs px-2 py-0.5 rounded-full bg-indigo-500/10 text-indigo-400 border border-indigo-500/20 font-medium">AI</span>
              </span>
              <span className="text-[10px] text-zinc-400 font-mono tracking-wider">CLAUDE-POWERED</span>
            </div>
          </div>

          {/* Desktop Navigation Links */}
          {activeView === 'landing' && (
            <nav className="hidden md:flex items-center gap-8 text-sm font-medium text-zinc-300 dark:text-zinc-300 light:text-zinc-600">
              <button 
                onClick={() => handleNavClick('features')} 
                className="hover:text-white dark:hover:text-white light:hover:text-black transition-colors"
              >
                Features
              </button>
              <button 
                onClick={() => handleNavClick('demo')} 
                className="hover:text-white dark:hover:text-white light:hover:text-black transition-colors flex items-center gap-1"
              >
                <Sparkles className="w-3.5 h-3.5 text-amber-400 animate-pulse" />
                Live Demo
              </button>
              <button 
                onClick={() => handleNavClick('testimonials')} 
                className="hover:text-white dark:hover:text-white light:hover:text-black transition-colors"
              >
                Wall of Love
              </button>
              <button 
                onClick={() => handleNavClick('pricing')} 
                className="hover:text-white dark:hover:text-white light:hover:text-black transition-colors"
              >
                Pricing
              </button>
            </nav>
          )}

          {/* Right Action Items & Theme Toggle */}
          <div className="hidden sm:flex items-center gap-3">
            {/* Theme Toggle Button */}
            <ThemeToggle />

            {isAuthenticated ? (
              <button
                onClick={() => navigateTo('app')}
                className="inline-flex items-center gap-2 px-4 py-2 rounded-xl text-sm font-semibold text-white bg-gradient-to-r from-indigo-600 to-purple-600 hover:from-indigo-500 hover:to-purple-500 shadow-md shadow-indigo-500/20 hover:shadow-indigo-500/30 transition-all cursor-pointer"
              >
                Go to Workspace
                <ArrowRight className="w-4 h-4" />
              </button>
            ) : (
              <>
                <button
                  onClick={() => navigateTo('auth', 'login')}
                  className="px-4 py-2 rounded-xl text-sm font-medium text-zinc-300 hover:text-white dark:text-zinc-300 dark:hover:text-white light:text-zinc-700 light:hover:text-black hover:bg-zinc-800/50 transition-all cursor-pointer"
                >
                  Log in
                </button>
                <button
                  onClick={() => navigateTo('auth', 'signup')}
                  className="inline-flex items-center gap-2 px-4 py-2 rounded-xl text-sm font-semibold text-white bg-indigo-600 hover:bg-indigo-500 shadow-md shadow-indigo-500/25 hover:shadow-indigo-500/40 transition-all cursor-pointer"
                >
                  Sign Up Free
                  <ArrowRight className="w-4 h-4" />
                </button>
              </>
            )}
          </div>

          {/* Mobile Menu & Theme Toggle */}
          <div className="flex sm:hidden items-center gap-2">
            <ThemeToggle />
            <button
              onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
              className="p-2 rounded-xl text-zinc-400 hover:text-white bg-zinc-900 border border-zinc-800"
            >
              {mobileMenuOpen ? <X className="w-5 h-5" /> : <Menu className="w-5 h-5" />}
            </button>
          </div>

        </div>
      </div>

      {/* Mobile Drawer Menu */}
      <AnimatePresence>
        {mobileMenuOpen && (
          <motion.div
            initial={{ opacity: 0, height: 0 }}
            animate={{ opacity: 1, height: 'auto' }}
            exit={{ opacity: 0, height: 0 }}
            className="sm:hidden border-b border-zinc-800 bg-zinc-950 px-4 pt-2 pb-6 space-y-3"
          >
            {activeView === 'landing' && (
              <div className="flex flex-col space-y-2 text-zinc-300 font-medium">
                <button 
                  onClick={() => handleNavClick('features')} 
                  className="text-left px-3 py-2 rounded-lg hover:bg-zinc-900"
                >
                  Features
                </button>
                <button 
                  onClick={() => handleNavClick('demo')} 
                  className="text-left px-3 py-2 rounded-lg hover:bg-zinc-900 flex items-center gap-2"
                >
                  <Sparkles className="w-4 h-4 text-amber-400" />
                  Live Demo
                </button>
                <button 
                  onClick={() => handleNavClick('testimonials')} 
                  className="text-left px-3 py-2 rounded-lg hover:bg-zinc-900"
                >
                  Testimonials
                </button>
                <button 
                  onClick={() => handleNavClick('pricing')} 
                  className="text-left px-3 py-2 rounded-lg hover:bg-zinc-900"
                >
                  Pricing
                </button>
              </div>
            )}

            <div className="pt-2 border-t border-zinc-800 flex flex-col gap-2">
              {isAuthenticated ? (
                <button
                  onClick={() => {
                    setMobileMenuOpen(false);
                    navigateTo('app');
                  }}
                  className="w-full text-center py-2.5 rounded-xl font-semibold text-white bg-indigo-600 hover:bg-indigo-500"
                >
                  Open Workspace
                </button>
              ) : (
                <>
                  <button
                    onClick={() => {
                      setMobileMenuOpen(false);
                      navigateTo('auth', 'login');
                    }}
                    className="w-full text-center py-2 rounded-xl text-zinc-300 bg-zinc-900 border border-zinc-800"
                  >
                    Log In
                  </button>
                  <button
                    onClick={() => {
                      setMobileMenuOpen(false);
                      navigateTo('auth', 'signup');
                    }}
                    className="w-full text-center py-2 rounded-xl font-semibold text-white bg-indigo-600"
                  >
                    Sign Up Free
                  </button>
                  <button
                    onClick={() => {
                      setMobileMenuOpen(false);
                      demoLogin();
                    }}
                    className="w-full text-center py-2 rounded-xl text-xs text-amber-300 bg-amber-500/10 border border-amber-500/20"
                  >
                    ⚡ Instant Demo Access
                  </button>
                </>
              )}
            </div>
          </motion.div>
        )}
      </AnimatePresence>
    </header>
  );
}
