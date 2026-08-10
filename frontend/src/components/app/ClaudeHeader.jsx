import React, { useState } from 'react';
import { 
  Bot, Menu, Download, FileText, CheckSquare, 
  MessageSquare, BarChart2, Search, Check 
} from 'lucide-react';

export default function ClaudeHeader({
  meeting,
  activeTab,
  onTabChange,
  onToggleMobileSidebar,
  onSearchChange,
  searchQuery
}) {
  const [copied, setCopied] = useState(false);

  const handleCopyMarkdown = () => {
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  return (
    <header className="bg-zinc-950 dark:bg-zinc-950 light:bg-white border-b border-zinc-800/80 light:border-zinc-200 px-4 py-3 sticky top-0 z-30">
      
      {/* Top Row: Mobile Menu + Title + Export Actions */}
      <div className="flex items-center justify-between gap-4">
        
        <div className="flex items-center gap-3">
          <button
            onClick={onToggleMobileSidebar}
            className="md:hidden p-2 rounded-xl text-zinc-400 hover:text-white bg-zinc-900 border border-zinc-800"
          >
            <Menu className="w-5 h-5" />
          </button>

          <div>
            <div className="flex items-center gap-2">
              <h1 className="font-bold text-base sm:text-lg text-white dark:text-white light:text-zinc-900 truncate max-w-xs sm:max-w-md">
                {meeting?.title || 'Database Meeting Analysis'}
              </h1>
              <span className="hidden sm:inline-flex items-center gap-1 px-2 py-0.5 rounded-full text-[10px] font-medium bg-emerald-500/10 text-emerald-400 border border-emerald-500/20">
                <span className="w-1.5 h-1.5 rounded-full bg-emerald-400 animate-pulse"></span>
                {meeting?.status || 'Active DB'}
              </span>
            </div>
            <p className="text-xs text-zinc-400 flex items-center gap-3 mt-0.5">
              <span>📅 {meeting?.date || (meeting?.created_at ? new Date(meeting.created_at).toLocaleDateString() : 'Live')}</span>
              <span>•</span>
              <span>⏱️ {meeting?.duration || (meeting?.duration_seconds ? `${Math.round(meeting.duration_seconds / 60)} mins` : 'Indexed')}</span>
              <span>•</span>
              <span className="text-indigo-400 font-mono uppercase">{meeting?.language || meeting?.category || 'RAG Vector'}</span>
            </p>
          </div>
        </div>

        {/* Right Tools & Export Dropdown */}
        <div className="flex items-center gap-2">
          
          {/* Quick Search */}
          <div className="relative hidden lg:block w-48">
            <Search className="w-3.5 h-3.5 text-zinc-500 absolute left-3 top-2.5" />
            <input
              type="text"
              placeholder="Search transcript..."
              value={searchQuery}
              onChange={(e) => onSearchChange(e.target.value)}
              className="w-full pl-8 pr-3 py-1.5 rounded-xl bg-zinc-900 border border-zinc-800 text-xs text-zinc-200 placeholder-zinc-500 focus:outline-none focus:border-indigo-500"
            />
          </div>

          <button
            onClick={handleCopyMarkdown}
            className="px-3 py-1.5 rounded-xl bg-zinc-900 hover:bg-zinc-800 text-zinc-300 border border-zinc-800 text-xs font-medium flex items-center gap-1.5 transition-colors cursor-pointer"
          >
            {copied ? <Check className="w-3.5 h-3.5 text-emerald-400" /> : <FileText className="w-3.5 h-3.5 text-indigo-400" />}
            <span className="hidden sm:inline">{copied ? 'Copied MD' : 'Copy MD'}</span>
          </button>

          <button
            onClick={() => alert('Exporting meeting summary & transcript from database...')}
            className="px-3 py-1.5 rounded-xl bg-indigo-600 hover:bg-indigo-500 text-white text-xs font-semibold flex items-center gap-1.5 shadow-md transition-colors cursor-pointer"
          >
            <Download className="w-3.5 h-3.5" />
            <span className="hidden sm:inline">Export PDF</span>
          </button>
        </div>

      </div>

      {/* Navigation Tabs Bar */}
      <div className="flex items-center gap-1 sm:gap-2 mt-4 pt-2 border-t border-zinc-800/60 overflow-x-auto scrollbar-none text-xs font-medium">
        <button
          onClick={() => onTabChange('chat')}
          className={`px-3 py-1.5 rounded-xl flex items-center gap-1.5 whitespace-nowrap transition-all ${
            activeTab === 'chat'
              ? 'bg-zinc-800 text-white border border-zinc-700 shadow-sm'
              : 'text-zinc-400 hover:text-zinc-200'
          }`}
        >
          <Bot className="w-3.5 h-3.5 text-purple-400" /> AI RAG Agent Chat
        </button>

        <button
          onClick={() => onTabChange('summary')}
          className={`px-3 py-1.5 rounded-xl flex items-center gap-1.5 whitespace-nowrap transition-all ${
            activeTab === 'summary'
              ? 'bg-zinc-800 text-white border border-zinc-700 shadow-sm'
              : 'text-zinc-400 hover:text-zinc-200'
          }`}
        >
          <FileText className="w-3.5 h-3.5 text-indigo-400" /> Executive Summary
        </button>

        <button
          onClick={() => onTabChange('actions')}
          className={`px-3 py-1.5 rounded-xl flex items-center gap-1.5 whitespace-nowrap transition-all ${
            activeTab === 'actions'
              ? 'bg-zinc-800 text-white border border-zinc-700 shadow-sm'
              : 'text-zinc-400 hover:text-zinc-200'
          }`}
        >
          <CheckSquare className="w-3.5 h-3.5 text-emerald-400" /> Action Items ({meeting?.actionItems?.length || 0})
        </button>

        <button
          onClick={() => onTabChange('transcript')}
          className={`px-3 py-1.5 rounded-xl flex items-center gap-1.5 whitespace-nowrap transition-all ${
            activeTab === 'transcript'
              ? 'bg-zinc-800 text-white border border-zinc-700 shadow-sm'
              : 'text-zinc-400 hover:text-zinc-200'
          }`}
        >
          <MessageSquare className="w-3.5 h-3.5 text-amber-400" /> Full Chunks / Transcript ({meeting?.transcript?.length || meeting?.total_chunks || 0})
        </button>

        <button
          onClick={() => onTabChange('analytics')}
          className={`px-3 py-1.5 rounded-xl flex items-center gap-1.5 whitespace-nowrap transition-all ${
            activeTab === 'analytics'
              ? 'bg-zinc-800 text-white border border-zinc-700 shadow-sm'
              : 'text-zinc-400 hover:text-zinc-200'
          }`}
        >
          <BarChart2 className="w-3.5 h-3.5 text-cyan-400" /> Speaker Analytics
        </button>
      </div>

    </header>
  );
}
