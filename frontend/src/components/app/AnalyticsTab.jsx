import React from 'react';
import { BarChart2, Users, PieChart, Clock, Award, Activity } from 'lucide-react';

export default function AnalyticsTab({ participants, duration }) {
  return (
    <div className="max-w-4xl mx-auto py-6 px-4 space-y-6 text-zinc-200">
      
      {/* Top Metrics Cards */}
      <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
        <div className="p-4 rounded-2xl bg-zinc-900 border border-zinc-800 space-y-1">
          <span className="text-xs font-mono text-zinc-400">Total Duration</span>
          <div className="text-xl font-bold text-white flex items-center gap-2">
            <Clock className="w-5 h-5 text-indigo-400" /> {duration}
          </div>
        </div>

        <div className="p-4 rounded-2xl bg-zinc-900 border border-zinc-800 space-y-1">
          <span className="text-xs font-mono text-zinc-400">Speaker Equilibrium</span>
          <div className="text-xl font-bold text-emerald-400 flex items-center gap-2">
            <Activity className="w-5 h-5" /> 89% Balanced
          </div>
        </div>

        <div className="p-4 rounded-2xl bg-zinc-900 border border-zinc-800 space-y-1">
          <span className="text-xs font-mono text-zinc-400">Speech Accuracy</span>
          <div className="text-xl font-bold text-indigo-300 flex items-center gap-2">
            <Award className="w-5 h-5 text-indigo-400" /> 98.4% WER
          </div>
        </div>
      </div>

      {/* Speaker Talk Time Progress Bars */}
      <div className="p-6 rounded-2xl bg-zinc-900 border border-zinc-800 space-y-4">
        <h3 className="text-base font-bold text-white flex items-center gap-2">
          <Users className="w-5 h-5 text-indigo-400" /> Speaker Time Distribution
        </h3>

        <div className="space-y-4">
          {participants.map((p, idx) => {
            const percentageVal = parseInt(p.timeSpoken.replace('%', '')) || 25;
            return (
              <div key={idx} className="space-y-1.5">
                <div className="flex items-center justify-between text-xs">
                  <div className="flex items-center gap-2">
                    <img src={p.avatar} alt={p.name} className="w-6 h-6 rounded-full object-cover" />
                    <span className="font-semibold text-white">{p.name}</span>
                    <span className="text-zinc-500">({p.role})</span>
                  </div>
                  <span className="font-mono text-indigo-400 font-bold">{p.timeSpoken}</span>
                </div>
                
                {/* Progress Bar */}
                <div className="w-full h-2.5 rounded-full bg-zinc-950 overflow-hidden border border-zinc-800">
                  <div
                    className="h-full bg-gradient-to-r from-indigo-500 to-emerald-400 rounded-full transition-all duration-500"
                    style={{ width: `${percentageVal}%` }}
                  />
                </div>
              </div>
            );
          })}
        </div>
      </div>

      {/* Topic Frequency Cloud */}
      <div className="p-6 rounded-2xl bg-zinc-900 border border-zinc-800 space-y-3">
        <h3 className="text-base font-bold text-white">Top Mentioned Keywords</h3>
        <div className="flex flex-wrap gap-2 pt-1">
          {['Whisper v3', 'Latency <300ms', 'WebSocket Stream', 'Claude 3.5 Sonnet', 'Jira Sync', 'Dark Theme UI', 'SOC2 Compliance', 'WebRTC Benchmark'].map((kw, i) => (
            <span key={i} className="px-3 py-1.5 rounded-xl bg-zinc-950 border border-zinc-800 text-xs font-mono text-indigo-300">
              #{kw}
            </span>
          ))}
        </div>
      </div>

    </div>
  );
}
