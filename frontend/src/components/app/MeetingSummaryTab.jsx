import React from 'react';
import { 
  Sparkles, CheckCircle2, Target, TrendingUp 
} from 'lucide-react';

export default function MeetingSummaryTab({ summary, title, participants }) {
  return (
    <div className="max-w-4xl mx-auto py-6 px-4 space-y-6 text-zinc-200">
      
      {/* Overview Header Card */}
      <div className="p-6 rounded-2xl bg-zinc-900 border border-zinc-800 shadow-lg space-y-4">
        <div className="flex items-center justify-between">
          <span className="inline-flex items-center gap-1.5 px-3 py-1 rounded-md text-xs font-semibold bg-indigo-950 text-indigo-400 border border-indigo-500/30">
            <Sparkles className="w-3.5 h-3.5" /> Executive Brief
          </span>
          <span className="text-xs font-mono text-zinc-400">Confidence Score: 99.2%</span>
        </div>

        <h2 className="text-xl sm:text-2xl font-bold text-white tracking-tight">{title}</h2>

        <p className="text-sm text-zinc-300 leading-relaxed font-normal">
          {summary.overview}
        </p>

        <div className="grid grid-cols-1 sm:grid-cols-2 gap-4 pt-2 border-t border-zinc-800">
          <div className="p-3 rounded-xl bg-zinc-950 border border-zinc-800">
            <span className="text-[11px] font-mono text-zinc-400 block mb-1">Meeting Sentiment</span>
            <span className="text-sm font-semibold text-emerald-400 flex items-center gap-1.5">
              <TrendingUp className="w-4 h-4" /> {summary.sentiment}
            </span>
          </div>

          <div className="p-3 rounded-xl bg-zinc-950 border border-zinc-800">
            <span className="text-[11px] font-mono text-zinc-400 block mb-1">Next Key Milestone</span>
            <span className="text-sm font-semibold text-indigo-400 flex items-center gap-1.5">
              <Target className="w-4 h-4 text-indigo-400" /> {summary.nextMilestone}
            </span>
          </div>
        </div>
      </div>

      {/* Key Takeaways Grid */}
      <div className="p-6 rounded-2xl bg-zinc-900 border border-zinc-800 space-y-4">
        <h3 className="text-base font-bold text-white flex items-center gap-2">
          <CheckCircle2 className="w-5 h-5 text-indigo-400" /> Key Strategic Decisions
        </h3>

        <div className="space-y-3">
          {summary.keyTakeaways.map((item, idx) => (
            <div key={idx} className="p-3.5 rounded-xl bg-zinc-950 border border-zinc-800 text-xs sm:text-sm text-zinc-300 flex items-start gap-3">
              <span className="w-6 h-6 rounded-md bg-indigo-600 text-white font-mono text-xs font-bold flex items-center justify-center shrink-0">
                {idx + 1}
              </span>
              <p className="leading-relaxed pt-0.5">{item}</p>
            </div>
          ))}
        </div>
      </div>

      {/* Participant Roster */}
      <div className="p-6 rounded-2xl bg-zinc-900 border border-zinc-800 space-y-4">
        <h3 className="text-base font-bold text-white">Attending Stakeholders</h3>
        <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
          {participants.map((p, idx) => (
            <div key={idx} className="p-3 rounded-xl bg-zinc-950 border border-zinc-800 flex items-center justify-between text-xs">
              <div className="flex items-center gap-3">
                <img src={p.avatar} alt={p.name} className="w-8 h-8 rounded-full object-cover border border-zinc-700" />
                <div>
                  <div className="font-semibold text-white">{p.name}</div>
                  <div className="text-zinc-400 text-[11px]">{p.role}</div>
                </div>
              </div>
              <span className="font-mono text-indigo-400 font-medium bg-indigo-950 px-2 py-0.5 rounded border border-indigo-500/30">
                {p.talkTimePercentage || 50}% speak time
              </span>
            </div>
          ))}
        </div>
      </div>

    </div>
  );
}
