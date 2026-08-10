import React, { useState } from 'react';
import { 
  Paperclip, Mic, Send, Sparkles, Zap, FileText, CheckSquare, Mail 
} from 'lucide-react';

export default function ClaudePromptInput({ onSendMessage, onQuickPrompt }) {
  const [prompt, setPrompt] = useState('');
  const [isRecording, setIsRecording] = useState(false);

  const handleSubmit = (e) => {
    e.preventDefault();
    if (!prompt.trim()) return;
    onSendMessage(prompt);
    setPrompt('');
  };

  const handleKeyDown = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSubmit(e);
    }
  };

  const quickPrompts = [
    { label: 'Summarize Decisions', icon: FileText, query: 'Extract all technical and product decisions from this meeting.' },
    { label: 'Extract Action Items', icon: CheckSquare, query: 'List all action items with their assigned owners and due dates.' },
    { label: 'Draft Follow-up Email', icon: Mail, query: 'Draft a concise executive follow-up email summarizing key outcomes.' }
  ];

  return (
    <div className="p-4 bg-zinc-950/90 backdrop-blur-xl border-t border-zinc-800/80 sticky bottom-0 z-20">
      <div className="max-w-4xl mx-auto space-y-3">
        
        {/* Quick Suggestion Pills */}
        <div className="flex items-center gap-2 overflow-x-auto scrollbar-none pb-1">
          <span className="text-[10px] font-mono text-zinc-500 uppercase tracking-wider shrink-0">Quick Prompts:</span>
          {quickPrompts.map((qp, idx) => {
            const Icon = qp.icon;
            return (
              <button
                key={idx}
                onClick={() => onQuickPrompt(qp.query)}
                className="px-2.5 py-1 rounded-full bg-zinc-900 hover:bg-zinc-800 border border-zinc-800 text-[11px] text-zinc-300 hover:text-white flex items-center gap-1.5 whitespace-nowrap transition-colors cursor-pointer"
              >
                <Icon className="w-3 h-3 text-indigo-400" />
                {qp.label}
              </button>
            );
          })}
        </div>

        {/* Input Box Container */}
        <form 
          onSubmit={handleSubmit}
          className="relative rounded-2xl bg-zinc-900 border border-zinc-800 focus-within:border-indigo-500/80 focus-within:ring-2 focus-within:ring-indigo-500/20 shadow-xl transition-all p-2 sm:p-3"
        >
          <textarea
            rows={2}
            value={prompt}
            onChange={(e) => setPrompt(e.target.value)}
            onKeyDown={handleKeyDown}
            placeholder="Ask Claude anything about this meeting, audio transcript, or action items... (Shift+Enter for new line)"
            className="w-full bg-transparent text-sm text-zinc-100 placeholder-zinc-500 focus:outline-none resize-none px-2"
          />

          <div className="flex items-center justify-between pt-2 border-t border-zinc-800/60 mt-1 px-1">
            
            <div className="flex items-center gap-2">
              <button
                type="button"
                onClick={() => alert('Audio file picker opened! Supports .mp3, .m4a, .wav')}
                className="p-1.5 rounded-lg text-zinc-400 hover:text-zinc-200 hover:bg-zinc-800 transition-colors"
                title="Attach audio or transcript file"
              >
                <Paperclip className="w-4 h-4" />
              </button>

              <button
                type="button"
                onClick={() => setIsRecording(!isRecording)}
                className={`p-1.5 rounded-lg transition-colors flex items-center gap-1.5 text-xs ${
                  isRecording 
                    ? 'bg-rose-500/20 text-rose-400 border border-rose-500/30 animate-pulse' 
                    : 'text-zinc-400 hover:text-zinc-200 hover:bg-zinc-800'
                }`}
                title="Voice input simulation"
              >
                <Mic className="w-4 h-4" />
                {isRecording && <span className="text-[10px] font-mono">Listening...</span>}
              </button>
            </div>

            <div className="flex items-center gap-2">
              <span className="text-[10px] font-mono text-zinc-500 hidden sm:inline">
                Claude 3.5 Sonnet Active
              </span>
              <button
                type="submit"
                disabled={!prompt.trim()}
                className={`p-2 rounded-xl text-white font-semibold transition-all cursor-pointer ${
                  prompt.trim()
                    ? 'bg-indigo-600 hover:bg-indigo-500 shadow-md shadow-indigo-600/30'
                    : 'bg-zinc-800 text-zinc-600 cursor-not-allowed'
                }`}
              >
                <Send className="w-4 h-4" />
              </button>
            </div>

          </div>
        </form>

      </div>
    </div>
  );
}
