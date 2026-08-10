import React from 'react';
import { useAuth } from '../../context/AuthContext';
import { GlowingHeroBg, GridPatternBackground } from './SvgBackgrounds';
import { 
  Sparkles, ArrowRight, Play, CheckCircle2, Bot, 
  Users, Zap 
} from 'lucide-react';
import { motion } from 'framer-motion';

export default function HeroSection() {
  const { navigateTo } = useAuth();

  return (
    <section className="relative pt-12 pb-20 md:pt-20 md:pb-32 overflow-hidden bg-zinc-950 text-white">
      {/* SVG Background Elements */}
      <GridPatternBackground />
      <GlowingHeroBg />

      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 relative z-10">
        
        {/* Top Announcement Pill */}
        <div className="flex justify-center mb-6">
          <motion.div
            initial={{ opacity: 0, y: -10 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.5 }}
            className="inline-flex items-center gap-2 px-3.5 py-1.5 rounded-full bg-zinc-900 border border-indigo-500/30 text-xs sm:text-sm text-zinc-300 shadow-lg backdrop-blur-md cursor-pointer hover:border-indigo-500/50 transition-colors"
            onClick={() => navigateTo('auth', 'signup')}
          >
            <span className="flex h-2 w-2 relative">
              <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-emerald-400 opacity-75"></span>
              <span className="relative inline-flex rounded-full h-2 w-2 bg-emerald-500"></span>
            </span>
            <span className="font-semibold text-zinc-100">MeetingSense 2.0 Live</span>
            <span className="text-zinc-600">|</span>
            <span className="text-indigo-400 flex items-center gap-1 font-medium">
              Claude 3.5 Sonnet Integration <Sparkles className="w-3.5 h-3.5 text-amber-400" />
            </span>
          </motion.div>
        </div>

        {/* Main Headline */}
        <div className="text-center max-w-4xl mx-auto space-y-6">
          <motion.h1 
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6, delay: 0.1 }}
            className="text-4xl sm:text-6xl lg:text-7xl font-extrabold tracking-tight text-white leading-[1.1]"
          >
            Turn Every Meeting into{' '}
            <span className="text-indigo-400 font-black">
              Structured Intelligence & Tasks
            </span>
          </motion.h1>

          <motion.p
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6, delay: 0.2 }}
            className="text-lg sm:text-xl text-zinc-400 max-w-2xl mx-auto leading-relaxed font-normal"
          >
            Stop taking notes manually. Our Claude-powered AI meeting assistant transcribes speech with 98.4% accuracy, detects speaker changes, extracts checkable action items, and answers queries in real time.
          </motion.p>

          {/* Action Buttons */}
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6, delay: 0.3 }}
            className="flex flex-col sm:flex-row items-center justify-center gap-4 pt-4"
          >
            <button
              onClick={() => navigateTo('auth', 'signup')}
              className="w-full sm:w-auto inline-flex items-center justify-center gap-2.5 px-7 py-3.5 rounded-2xl text-base font-semibold text-white bg-indigo-600 hover:bg-indigo-500 shadow-lg shadow-indigo-600/25 transition-all cursor-pointer"
            >
              Start Free Trial
              <ArrowRight className="w-5 h-5" />
            </button>

            <button
              onClick={() => {
                const el = document.getElementById('demo');
                if (el) el.scrollIntoView({ behavior: 'smooth' });
              }}
              className="w-full sm:w-auto inline-flex items-center justify-center gap-2 px-5 py-3.5 rounded-2xl text-sm font-medium text-zinc-300 hover:text-white bg-zinc-900 border border-zinc-800 hover:border-zinc-700 transition-all cursor-pointer"
            >
              <Play className="w-4 h-4 text-emerald-400 fill-emerald-400" />
              Watch Interactive Demo
            </button>
          </motion.div>

          {/* Social Proof Tags */}
          <motion.div 
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            transition={{ duration: 0.6, delay: 0.4 }}
            className="flex flex-wrap items-center justify-center gap-6 pt-4 text-xs text-zinc-400 font-medium"
          >
            <span className="flex items-center gap-1.5">
              <CheckCircle2 className="w-4 h-4 text-emerald-400" /> No credit card required
            </span>
            <span className="flex items-center gap-1.5">
              <CheckCircle2 className="w-4 h-4 text-emerald-400" /> SOC2 Type II Certified
            </span>
            <span className="flex items-center gap-1.5">
              <CheckCircle2 className="w-4 h-4 text-emerald-400" /> 1-Click Jira & Slack Export
            </span>
          </motion.div>

        </div>

        {/* Live Interface Preview Mockup Card */}
        <motion.div
          initial={{ opacity: 0, y: 40 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.8, delay: 0.5 }}
          className="mt-14 max-w-5xl mx-auto"
        >
          <div className="relative rounded-2xl p-1 bg-zinc-900 border border-zinc-800 shadow-2xl">
            <div className="rounded-[14px] bg-zinc-950 border border-zinc-800 overflow-hidden shadow-inner">
              
              {/* Window Header */}
              <div className="px-4 py-3 bg-zinc-900 border-b border-zinc-800 flex items-center justify-between">
                <div className="flex items-center gap-2">
                  <div className="w-3 h-3 rounded-full bg-rose-500/80"></div>
                  <div className="w-3 h-3 rounded-full bg-amber-500/80"></div>
                  <div className="w-3 h-3 rounded-full bg-emerald-500/80"></div>
                  <span className="ml-2 text-xs font-mono text-zinc-400 hidden sm:inline">
                    MeetingSense AI Workspace — Claude 3.5 Active
                  </span>
                </div>
                <div className="flex items-center gap-2">
                  <span className="inline-flex items-center gap-1.5 px-2.5 py-0.5 rounded-full text-[11px] font-medium bg-emerald-950 text-emerald-400 border border-emerald-500/30">
                    <span className="w-1.5 h-1.5 rounded-full bg-emerald-400 animate-pulse"></span>
                    Live Audio Stream (&lt;300ms)
                  </span>
                </div>
              </div>

              {/* Mockup Dashboard Interior */}
              <div className="p-4 sm:p-6 grid grid-cols-1 md:grid-cols-12 gap-4 bg-zinc-950">
                
                {/* Left Sidebar Mock */}
                <div className="hidden md:block md:col-span-4 bg-zinc-900 rounded-xl p-3 border border-zinc-800 space-y-3">
                  <div className="text-xs font-semibold text-zinc-400 tracking-wider uppercase px-2">Active Session</div>
                  <div className="p-2.5 rounded-lg bg-zinc-850 border border-indigo-500/40 text-xs">
                    <div className="font-semibold text-zinc-100 flex items-center justify-between">
                      <span>Q3 Product & AI Roadmap</span>
                      <span className="text-[10px] text-indigo-400 bg-indigo-950 px-1.5 py-0.5 rounded border border-indigo-500/30 font-semibold">Live</span>
                    </div>
                    <div className="text-zinc-400 mt-1 flex items-center gap-2">
                      <Users className="w-3 h-3 text-zinc-500" /> 4 Participants • 42m
                    </div>
                  </div>

                  <div className="space-y-1 pt-2">
                    <div className="text-[11px] text-zinc-400 font-medium px-2">Extracted Action Items (3/4)</div>
                    <div className="p-2 rounded bg-zinc-950 border border-zinc-800 text-[11px] text-zinc-300 flex items-start gap-2">
                      <input type="checkbox" checked readOnly className="mt-0.5 accent-indigo-600 rounded" />
                      <div>
                        <span className="line-through text-zinc-500">Benchmark WebRTC latency</span>
                        <span className="block text-[9px] text-indigo-400 font-mono">Owner: Marcus Chen</span>
                      </div>
                    </div>
                    <div className="p-2 rounded bg-zinc-950 border border-zinc-800 text-[11px] text-zinc-300 flex items-start gap-2">
                      <input type="checkbox" readOnly className="mt-0.5 accent-indigo-600 rounded" />
                      <div>
                        <span>Draft API contracts for Slack hook</span>
                        <span className="block text-[9px] text-amber-400 font-mono">Owner: Alex Rivera • Due Aug 16</span>
                      </div>
                    </div>
                  </div>
                </div>

                {/* Right Chat Mock */}
                <div className="md:col-span-8 space-y-3">
                  {/* User query bubble */}
                  <div className="flex items-start gap-2.5 justify-end">
                    <div className="bg-zinc-900 border border-indigo-500/40 text-zinc-100 rounded-2xl rounded-tr-none px-4 py-2.5 text-xs max-w-sm">
                      Summarize technical decisions on audio streaming latency.
                    </div>
                    <div className="w-7 h-7 rounded-full bg-indigo-600 flex items-center justify-center text-[10px] font-bold text-white">
                      YOU
                    </div>
                  </div>

                  {/* Claude Assistant bubble */}
                  <div className="flex items-start gap-2.5">
                    <div className="w-7 h-7 rounded-full bg-zinc-900 border border-emerald-500/40 flex items-center justify-center">
                      <Bot className="w-3.5 h-3.5 text-emerald-400" />
                    </div>
                    <div className="bg-zinc-900 border border-zinc-800 text-zinc-200 rounded-2xl rounded-tl-none p-4 text-xs space-y-2 max-w-md">
                      <div className="flex items-center gap-2 text-[10px] font-mono text-emerald-400 font-medium">
                        <Sparkles className="w-3 h-3" /> Claude RAG Agent Response
                      </div>
                      <p className="leading-relaxed">
                        **Speech Latency Decision**: Standardized on WebSocket audio chunking with **Whisper-Large-v3** targeting **&lt;300ms** latency with **98.4%** word error accuracy.
                      </p>
                      <div className="p-2 rounded bg-zinc-950 font-mono text-[10px] text-indigo-300 border border-zinc-800">
                        {`{ "latency": "<300ms", "accuracy": "98.4%", "model": "whisper-v3" }`}
                      </div>
                    </div>
                  </div>

                </div>

              </div>

            </div>
          </div>
        </motion.div>

      </div>
    </section>
  );
}
