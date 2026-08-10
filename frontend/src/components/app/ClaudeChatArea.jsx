import React from 'react';
import { Bot, User, Sparkles, Copy, Check, CornerDownRight } from 'lucide-react';
import { useState } from 'react';

export default function ClaudeChatArea({ messages, onQuickPrompt }) {
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
              className={`w-8 h-8 rounded-full flex items-center justify-center shrink-0 border shadow-md ${
                isUser
                  ? 'bg-indigo-600 border-indigo-400/40 text-white font-bold text-xs'
                  : 'bg-zinc-900 border-emerald-500/30 text-emerald-400'
              }`}
            >
              {isUser ? 'YOU' : <Bot className="w-4 h-4 text-emerald-400" />}
            </div>

            {/* Content Bubble */}
            <div
              className={`flex-1 rounded-2xl p-4 sm:p-5 text-xs sm:text-sm border shadow-lg leading-relaxed ${
                isUser
                  ? 'bg-indigo-600/20 border-indigo-500/30 text-indigo-100 max-w-2xl ml-auto rounded-tr-none'
                  : 'bg-zinc-900/90 border-zinc-800 text-zinc-200 rounded-tl-none space-y-3'
              }`}
            >
              {/* Header Info */}
              <div className="flex items-center justify-between text-[11px] font-mono text-zinc-500 pb-2 border-b border-zinc-800/60">
                <span className="flex items-center gap-1.5">
                  {isUser ? (
                    'User Query'
                  ) : (
                    <>
                      <Sparkles className="w-3 h-3 text-emerald-400" />
                      Claude 3.5 Sonnet
                    </>
                  )}
                </span>
                <span>{m.time}</span>
              </div>

              {/* Message Body */}
              <div className="whitespace-pre-line space-y-2 font-sans">
                {m.text}
              </div>

              {/* Assistant Message Footer Toolbar */}
              {!isUser && (
                <div className="pt-2 border-t border-zinc-800/60 flex items-center justify-between text-[11px] text-zinc-500">
                  <span className="flex items-center gap-1 text-emerald-400 font-mono">
                    <Check className="w-3 h-3" /> Grounded in audio transcript
                  </span>
                  <button
                    onClick={() => handleCopy(m.id, m.text)}
                    className="flex items-center gap-1 text-zinc-400 hover:text-white transition-colors"
                  >
                    {copiedId === m.id ? (
                      <span className="text-emerald-400">Copied!</span>
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
    </div>
  );
}
