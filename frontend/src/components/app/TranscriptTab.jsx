import React, { useState } from 'react';
import { Search, MessageSquare, Clock, User, Volume2 } from 'lucide-react';

export default function TranscriptTab({ transcript, searchQuery = '' }) {
  const [localSearch, setLocalSearch] = useState(searchQuery);

  const filteredLines = transcript.filter((t) => {
    if (!localSearch) return true;
    return (
      t.text.toLowerCase().includes(localSearch.toLowerCase()) ||
      t.speaker.toLowerCase().includes(localSearch.toLowerCase())
    );
  });

  return (
    <div className="max-w-4xl mx-auto py-6 px-4 space-y-6 text-zinc-200">
      
      {/* Search Header */}
      <div className="p-4 rounded-2xl bg-zinc-900 border border-zinc-800 flex items-center gap-3">
        <Search className="w-4 h-4 text-zinc-400" />
        <input
          type="text"
          placeholder="Filter transcript by keyword or speaker name..."
          value={localSearch}
          onChange={(e) => setLocalSearch(e.target.value)}
          className="w-full bg-transparent text-xs text-white placeholder-zinc-500 focus:outline-none"
        />
        {localSearch && (
          <button
            onClick={() => setLocalSearch('')}
            className="text-xs text-zinc-400 hover:text-white"
          >
            Clear
          </button>
        )}
      </div>

      {/* Transcript Timeline List */}
      <div className="space-y-3">
        {filteredLines.map((t) => (
          <div
            key={t.id}
            className="p-4 rounded-2xl bg-zinc-900/80 border border-zinc-800/80 hover:border-zinc-700 transition-colors space-y-2"
          >
            <div className="flex items-center justify-between">
              <div className="flex items-center gap-2">
                <span className="w-2 h-2 rounded-full bg-indigo-500"></span>
                <span className="font-semibold text-xs text-white">{t.speaker}</span>
              </div>
              <button
                onClick={() => alert(`Seeking audio to ${t.timestamp}`)}
                className="font-mono text-[11px] text-zinc-500 hover:text-indigo-400 flex items-center gap-1 transition-colors"
              >
                <Clock className="w-3 h-3" /> {t.timestamp}
              </button>
            </div>

            <p className="text-xs sm:text-sm text-zinc-300 leading-relaxed font-sans pl-4 border-l-2 border-indigo-500/30">
              {t.text}
            </p>
          </div>
        ))}

        {filteredLines.length === 0 && (
          <div className="text-center py-12 text-zinc-500 text-xs">
            No transcript entries match "{localSearch}".
          </div>
        )}
      </div>

    </div>
  );
}
