import React, { useState } from 'react';
import { Bot, Sparkles, Copy, Check, Loader2 } from 'lucide-react';

export default function ClaudeChatArea({ messages, isGenerating }) {
  const [copiedId, setCopiedId] = useState(null);

  const handleCopy = (id, text) => {
    navigator.clipboard.writeText(text);
    setCopiedId(id);
    setTimeout(() => setCopiedId(null), 2000);
  };

  return (
    <div className="space-y-6 max-w-4xl mx-auto py-6 px-4">
      {messages.map((m) => {
        const isUser = m.sender === 'user';
        return (
          <div
            key={m.id}
            className={`flex items-start gap-3 sm:gap-4 ${
              isUser ? 'flex-row-reverse' : 'flex-row'
            }`}
          >
            {/* Avatar */}
            <div
              className={`w-8 h-8 rounded-full flex items-center justify-center shrink-0 border ${
                isUser
                  ? 'bg-indigo-600 border-indigo-500 text-white font-bold text-xs'
                  : 'bg-zinc-900 border-emerald-500/40 text-emerald-400'
              }`}
            >
              {isUser ? 'YOU' : <Bot className="w-4 h-4 text-emerald-400" />}
            </div>

            {/* Content Bubble */}
            <div
              className={`flex-1 rounded-2xl p-4 sm:p-5 text-xs sm:text-sm border leading-relaxed ${
                isUser
                  ? 'bg-zinc-900 border-indigo-500/40 text-zinc-100 max-w-2xl ml-auto rounded-tr-none'
                  : 'bg-zinc-900 border-zinc-800 text-zinc-200 rounded-tl-none space-y-3'
              }`}
            >
              {/* Header Info */}
              <div className="flex items-center justify-between text-[11px] font-mono text-zinc-500 pb-2 border-b border-zinc-800">
                <span className="flex items-center gap-1.5">
                  {isUser ? (
                    'User Query'
                  ) : (
                    <>
                      <Sparkles className="w-3 h-3 text-emerald-400" />
                      Claude RAG Agent
                    </>
                  )}
                </span>
                <span>{m.time}</span>
              </div>

              {/* Message Body */}
              <div className="whitespace-pre-line space-y-2 font-sans text-zinc-200 leading-relaxed">
                {m.text}
              </div>

              {/* Assistant Message Footer Toolbar */}
              {!isUser && (
                <div className="pt-2 border-t border-zinc-800 flex items-center justify-between text-[11px] text-zinc-500">
                  <span className="flex items-center gap-1 text-emerald-400 font-mono font-medium">
                    <Check className="w-3 h-3" /> Grounded in Supabase DB & Pinecone vectors
                  </span>
                  <button
                    onClick={() => handleCopy(m.id, m.text)}
                    className="flex items-center gap-1 text-zinc-400 hover:text-white transition-colors cursor-pointer"
                  >
                    {copiedId === m.id ? (
                      <span className="text-emerald-400 font-semibold">Copied!</span>
                    ) : (
                      <>
                        <Copy className="w-3 h-3" /> Copy Response
                      </>
                    )}
                  </button>
                </div>
              )}
            </div>
          </div>
        );
      })}

      {/* Streaming Skeleton Indicator while model is responding */}
      {isGenerating && (
        <div className="flex items-start gap-3 sm:gap-4 animate-pulse">
          <div className="w-8 h-8 rounded-full bg-indigo-600 border border-indigo-400 flex items-center justify-center shrink-0 text-white">
            <Loader2 className="w-4 h-4 animate-spin" />
          </div>
          <div className="flex-1 rounded-2xl p-5 bg-zinc-900 border border-zinc-800 space-y-3 rounded-tl-none">
            <div className="flex items-center justify-between text-[11px] font-mono text-indigo-400 pb-2 border-b border-zinc-800">
              <span className="flex items-center gap-2">
                <Sparkles className="w-3.5 h-3.5 text-indigo-400 animate-spin" />
                Claude RAG Agent is analyzing Pinecone vectors & generating response...
              </span>
              <span className="bg-indigo-950 text-indigo-300 px-2 py-0.5 rounded text-[10px] font-bold uppercase">Processing</span>
            </div>
            <div className="space-y-2 pt-1">
              <div className="h-3.5 bg-zinc-800 rounded w-full"></div>
              <div className="h-3.5 bg-zinc-800 rounded w-5/6"></div>
              <div className="h-3.5 bg-zinc-850 rounded w-3/4"></div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
