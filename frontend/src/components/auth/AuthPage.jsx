import React, { useState } from 'react';
import { useAuth } from '../../context/AuthContext';
import Navbar from '../common/Navbar';
import Footer from '../common/Footer';
import { GridPatternBackground, GlowingHeroBg } from '../landing/SvgBackgrounds';
import { 
  Bot, Mail, Lock, User, Briefcase, Eye, EyeOff, 
  ArrowRight, Zap, CheckCircle2, AlertCircle, ArrowLeft
} from 'lucide-react';
import { motion, AnimatePresence } from 'framer-motion';

export default function AuthPage() {
  const { authTab, setAuthTab, login, signup, resetPassword, navigateTo, error, setError, loading } = useAuth();
  
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [name, setName] = useState('');
  const [role, setRole] = useState('Product Lead');
  const [showPassword, setShowPassword] = useState(false);
  const [resetSentMessage, setResetSentMessage] = useState(null);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError(null);
    setResetSentMessage(null);

    if (authTab === 'forgot_password') {
      const res = await resetPassword(email);
      if (res.success) {
        setResetSentMessage(res.message);
      }
    } else if (authTab === 'login') {
      await login(email, password);
    } else {
      await signup(name, email, password, role);
    }
  };

  return (
    <div className="min-h-screen bg-zinc-950 text-white flex flex-col justify-between selection:bg-indigo-500 selection:text-white">
      <Navbar />

      <main className="relative flex-grow flex items-center justify-center py-12 px-4 sm:px-6 lg:px-8">
        <GridPatternBackground />
        <GlowingHeroBg />

        <motion.div 
          initial={{ opacity: 0, scale: 0.95 }}
          animate={{ opacity: 1, scale: 1 }}
          transition={{ duration: 0.4 }}
          className="w-full max-w-md relative z-10"
        >
          {/* Card Wrapper */}
          <div className="bg-zinc-900/90 border border-zinc-800 rounded-3xl p-6 sm:p-8 shadow-2xl backdrop-blur-xl">
            
            {/* Header Brand */}
            <div className="text-center space-y-2 mb-6">
              <div 
                onClick={() => navigateTo('landing')}
                className="inline-flex items-center gap-2 cursor-pointer group"
              >
                <div className="w-10 h-10 rounded-xl bg-indigo-600 flex items-center justify-center text-white shadow-md">
                  <Bot className="w-5 h-5" />
                </div>
                <span className="font-bold text-xl text-white tracking-tight">MeetingSense AI</span>
              </div>
              
              <h2 className="text-2xl font-bold text-white tracking-tight">
                {authTab === 'forgot_password'
                  ? 'Reset Your Password'
                  : authTab === 'login' 
                  ? 'Welcome Back to Your Workspace' 
                  : 'Create Your Free Account'}
              </h2>
              <p className="text-xs text-zinc-400">
                {authTab === 'forgot_password'
                  ? 'Enter your account email to receive a password reset link via Supabase Auth.'
                  : authTab === 'login' 
                  ? 'Access your meetings, Claude summaries, and action items.' 
                  : 'Start transcribing speech with Claude 3.5 Sonnet in seconds.'}
              </p>
            </div>

            {/* Error or Success Banners */}
            {error && (
              <div className="mb-4 p-3 bg-rose-500/10 border border-rose-500/30 rounded-xl text-xs text-rose-400 flex items-center gap-2">
                <AlertCircle className="w-4 h-4 shrink-0" />
                <span>{error}</span>
              </div>
            )}

            {resetSentMessage && (
              <div className="mb-4 p-3 bg-emerald-500/10 border border-emerald-500/30 rounded-xl text-xs text-emerald-400 flex items-center gap-2">
                <CheckCircle2 className="w-4 h-4 shrink-0" />
                <span>{resetSentMessage}</span>
              </div>
            )}

            {/* Auth Tab Switcher */}
            {authTab !== 'forgot_password' && (
              <div className="grid grid-cols-2 p-1 rounded-xl bg-zinc-950 border border-zinc-800 mb-6">
                <button
                  type="button"
                  onClick={() => setAuthTab('login')}
                  className={`py-2 text-xs font-semibold rounded-lg transition-all ${
                    authTab === 'login'
                      ? 'bg-zinc-800 text-white shadow-md'
                      : 'text-zinc-400 hover:text-zinc-200'
                  }`}
                >
                  Log In
                </button>
                <button
                  type="button"
                  onClick={() => setAuthTab('signup')}
                  className={`py-2 text-xs font-semibold rounded-lg transition-all ${
                    authTab === 'signup'
                      ? 'bg-zinc-800 text-white shadow-md'
                      : 'text-zinc-400 hover:text-zinc-200'
                  }`}
                >
                  Sign Up
                </button>
              </div>
            )}

            {/* Form */}
            <form onSubmit={handleSubmit} className="space-y-4">
              <AnimatePresence mode="wait">
                {authTab === 'signup' && (
                  <motion.div
                    key="signup-fields"
                    initial={{ opacity: 0, height: 0 }}
                    animate={{ opacity: 1, height: 'auto' }}
                    exit={{ opacity: 0, height: 0 }}
                    className="space-y-4 overflow-hidden"
                  >
                    <div>
                      <label className="block text-xs font-medium text-zinc-300 mb-1">Full Name</label>
                      <div className="relative">
                        <User className="w-4 h-4 text-zinc-500 absolute left-3.5 top-3" />
                        <input
                          type="text"
                          required
                          value={name}
                          onChange={(e) => setName(e.target.value)}
                          placeholder="Ravi Kumar"
                          className="w-full pl-10 pr-4 py-2.5 rounded-xl bg-zinc-950 border border-zinc-800 text-xs text-white placeholder-zinc-500 focus:outline-none focus:border-indigo-500 transition-colors"
                        />
                      </div>
                    </div>

                    <div>
                      <label className="block text-xs font-medium text-zinc-300 mb-1">Role / Position</label>
                      <div className="relative">
                        <Briefcase className="w-4 h-4 text-zinc-500 absolute left-3.5 top-3" />
                        <select
                          value={role}
                          onChange={(e) => setRole(e.target.value)}
                          className="w-full pl-10 pr-4 py-2.5 rounded-xl bg-zinc-950 border border-zinc-800 text-xs text-white focus:outline-none focus:border-indigo-500 transition-colors"
                        >
                          <option value="Product Lead">Product Lead / PM</option>
                          <option value="Engineering Lead">Engineering Director</option>
                          <option value="UX Researcher">UX Researcher</option>
                          <option value="Executive">Executive / C-Suite</option>
                          <option value="Freelancer">Freelancer / Independent</option>
                        </select>
                      </div>
                    </div>
                  </motion.div>
                )}
              </AnimatePresence>

              <div>
                <label className="block text-xs font-medium text-zinc-300 mb-1">Work Email</label>
                <div className="relative">
                  <Mail className="w-4 h-4 text-zinc-500 absolute left-3.5 top-3" />
                  <input
                    type="email"
                    required
                    value={email}
                    onChange={(e) => setEmail(e.target.value)}
                    placeholder="user@example.com"
                    className="w-full pl-10 pr-4 py-2.5 rounded-xl bg-zinc-950 border border-zinc-800 text-xs text-white placeholder-zinc-500 focus:outline-none focus:border-indigo-500 transition-colors"
                  />
                </div>
              </div>

              {authTab !== 'forgot_password' && (
                <div>
                  <div className="flex items-center justify-between mb-1">
                    <label className="block text-xs font-medium text-zinc-300">Password</label>
                    {authTab === 'login' && (
                      <button
                        type="button"
                        onClick={() => { setAuthTab('forgot_password'); setError(null); setResetSentMessage(null); }}
                        className="text-[11px] text-indigo-400 hover:underline cursor-pointer"
                      >
                        Forgot password?
                      </button>
                    )}
                  </div>
                  <div className="relative">
                    <Lock className="w-4 h-4 text-zinc-500 absolute left-3.5 top-3" />
                    <input
                      type={showPassword ? 'text' : 'password'}
                      required
                      value={password}
                      onChange={(e) => setPassword(e.target.value)}
                      placeholder="••••••••••••"
                      className="w-full pl-10 pr-10 py-2.5 rounded-xl bg-zinc-950 border border-zinc-800 text-xs text-white placeholder-zinc-500 focus:outline-none focus:border-indigo-500 transition-colors"
                    />
                    <button
                      type="button"
                      onClick={() => setShowPassword(!showPassword)}
                      className="absolute right-3.5 top-3 text-zinc-500 hover:text-zinc-300"
                    >
                      {showPassword ? <EyeOff className="w-4 h-4" /> : <Eye className="w-4 h-4" />}
                    </button>
                  </div>
                </div>
              )}

              <button
                type="submit"
                disabled={loading}
                className="w-full py-3 px-4 rounded-xl text-xs font-semibold text-white bg-indigo-600 hover:bg-indigo-500 shadow-lg shadow-indigo-600/30 transition-all flex items-center justify-center gap-2 cursor-pointer mt-2"
              >
                {loading ? (
                  <span className="flex items-center gap-2">
                    <span className="w-4 h-4 border-2 border-white border-t-transparent rounded-full animate-spin"></span>
                    Processing...
                  </span>
                ) : (
                  <>
                    {authTab === 'forgot_password'
                      ? 'Send Password Reset Email'
                      : authTab === 'login' 
                      ? 'Log In via Supabase Auth' 
                      : 'Create Supabase Account'}
                    <ArrowRight className="w-4 h-4" />
                  </>
                )}
              </button>
            </form>

            {authTab === 'forgot_password' && (
              <div className="mt-4 text-center">
                <button
                  type="button"
                  onClick={() => { setAuthTab('login'); setError(null); setResetSentMessage(null); }}
                  className="text-xs text-zinc-400 hover:text-white flex items-center justify-center gap-1.5 mx-auto"
                >
                  <ArrowLeft className="w-3.5 h-3.5" /> Back to Log In
                </button>
              </div>
            )}

            {/* Social Divider */}
            {authTab !== 'forgot_password' && (
              <>
                <div className="my-6 flex items-center gap-3">
                  <div className="flex-1 h-px bg-zinc-800"></div>
                  <span className="text-[11px] text-zinc-500 font-mono">OR CONTINUE WITH</span>
                  <div className="flex-1 h-px bg-zinc-800"></div>
                </div>

                {/* Social Buttons */}
                <div className="grid grid-cols-2 gap-3">
                  <button
                    type="button"
                    onClick={() => setError('Google SSO requires OAuth provider keys configured in your Supabase project dashboard.')}
                    className="py-2.5 px-3 rounded-xl bg-zinc-950 border border-zinc-800 hover:border-zinc-700 text-xs font-medium text-zinc-300 flex items-center justify-center gap-2 transition-colors cursor-pointer"
                  >
                    <svg className="w-4 h-4" viewBox="0 0 24 24">
                      <path fill="#EA4335" d="M12 5c1.6 0 3 .6 4.1 1.6l3.1-3.1C17.3 1.7 14.8 1 12 1 7.5 1 3.7 3.6 1.9 7.3l3.7 2.9C6.5 7.2 9 5 12 5z" />
                      <path fill="#4285F4" d="M23.5 12.3c0-.8-.1-1.6-.2-2.3H12v4.5h6.5c-.3 1.5-1.1 2.8-2.4 3.7l3.7 2.9c2.2-2 3.7-5 3.7-8.8z" />
                      <path fill="#FBBC05" d="M5.6 14.8c-.2-.7-.4-1.5-.4-2.3s.2-1.6.4-2.3L1.9 7.3C.7 9.7 0 10.8 0 12s.7 2.3 1.9 4.7l3.7-2.9z" />
                      <path fill="#34A853" d="M12 23c3.2 0 6-1.1 8-3l-3.7-2.9c-1.1.7-2.5 1.2-4.3 1.2-3 0-5.5-2.2-6.4-5.2L1.9 16C3.7 19.7 7.5 23 12 23z" />
                    </svg>
                    Google SSO
                  </button>

                  <button
                    type="button"
                    onClick={() => setError('GitHub OAuth requires provider keys configured in your Supabase project dashboard.')}
                    className="py-2.5 px-3 rounded-xl bg-zinc-950 border border-zinc-800 hover:border-zinc-700 text-xs font-medium text-zinc-300 flex items-center justify-center gap-2 transition-colors cursor-pointer"
                  >
                    <svg className="w-4 h-4 text-white fill-current" viewBox="0 0 24 24">
                      <path d="M12 0C5.37 0 0 5.37 0 12c0 5.31 3.435 9.795 8.205 11.385.6.105.825-.255.825-.57 0-.285-.015-1.23-.015-2.235-3.015.555-3.795-.735-4.035-1.41-.135-.345-.72-1.41-1.23-1.695-.42-.225-1.02-.78-.015-.795.945-.015 1.62.87 1.845 1.23 1.08 1.815 2.805 1.305 3.495.99.105-.78.42-1.305.765-1.605-2.67-.3-5.46-1.335-5.46-5.925 0-1.305.465-2.385 1.23-3.225-.12-.3-.54-1.53.12-3.18 0 0 1.005-.315 3.3 1.23.96-.27 1.98-.405 3-.405s2.04.135 3 .405c2.295-1.56 3.3-1.23 3.3-1.23.66 1.65.24 2.88.12 3.18.765.84 1.23 1.905 1.23 3.225 0 4.605-2.805 5.625-5.475 5.925.435.375.81 1.095.81 2.22 0 1.605-.015 2.895-.015 3.3 0 .315.225.69.825.57A12.02 12.02 0 0024 12c0-6.63-5.37-12-12-12z"/>
                    </svg>
                    GitHub
                  </button>
                </div>
              </>
            )}

          </div>
        </motion.div>
      </main>

      <Footer />
    </div>
  );
}
