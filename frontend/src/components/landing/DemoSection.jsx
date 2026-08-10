import React, { useState, useEffect } from 'react';
import { 
  Play, Pause, Sparkles, CheckSquare, MessageSquare, 
  FileText, Users, Bot, ArrowRight, Zap 
} from 'lucide-react';
import { motion, AnimatePresence } from 'framer-motion';
import { useAuth } from '../../context/AuthContext';
import { api } from '../../services/api';

export default function DemoSection() {
  const { navigateTo } = useAuth();
  const [meetings, setMeetings] = useState([]);
  const [selectedMeeting, setSelectedMeeting] = useState(null);
  const [activeTab, setActiveTab] = useState('summary');
  const [isPlaying, setIsPlaying] = useState(false);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    api.getMeetings()
      .then((res) => {
        const dbData = res.data || [];
        setMeetings(dbData);
        if (dbData.length > 0) {
          const m = dbData[0];
          setSelectedMeeting({
            id: m.id,
            title: m.title,
            date: m.created_at ? new Date(m.created_at).toLocaleDateString() : 'Live DB',
            duration: m.duration_seconds ? `${Math.round(m.duration_seconds / 60)} mins` : `${m.total_chunks || 20} Chunks`,
            category: m.language?.toUpperCase() || 'RAG DB',
            summary: {
              overview: `Live Supabase Database entry: '${m.title}'. Ingested source ${m.source_url || 'transcript'} into Pinecone vector index.`,
              keyTakeaways: [
                `Total Chunks: ${m.total_chunks || 20}`,
                `Status: ${m.status || 'ready'}`,
                `Vector Namespace: ${m.pinecone_namespace || m.id}`
              ],
              sentiment: 'Positive & High Impact',
              nextMilestone: 'Live Agent Chat'
            },
            actionItems: [
              { id: 'a1', task: 'Verify vector embeddings in Pinecone DB', owner: 'Ravi Kumar', dueDate: 'Today', priority: 'High', completed: false },
              { id: 'a2', task: 'Execute cross-meeting trend query', owner: 'Engineering Lead', dueDate: 'Tomorrow', priority: 'Medium', completed: true },
            ],
            transcript: [
              { id: 't1', speaker: 'Speaker 1', time: '00:15', text: 'Supabase database is connected and storing all meeting transcript chunks.' },
              { id: 't2', speaker: 'Speaker 2', time: '00:45', text: 'FastAPI backend executes RAG searches directly against Pinecone vector namespaces.' }
            ]
          });
        }
      })
      .catch((err) => {
        console.warn('Demo section DB fetch notice:', err);
      })
      .finally(() => setLoading(false));
  }, []);

  const handleSelectDbMeeting = (m) => {
    setSelectedMeeting({
      id: m.id,
      title: m.title,
      date: m.created_at ? new Date(m.created_at).toLocaleDateString() : 'Live DB',
      duration: m.duration_seconds ? `${Math.round(m.duration_seconds / 60)} mins` : `${m.total_chunks || 20} Chunks`,
      category: m.language?.toUpperCase() || 'RAG DB',
      summary: {
        overview: `Supabase Database session '${m.title}'. Vector store namespace: ${m.pinecone_namespace || m.id}.`,
        keyTakeaways: [
          `Total Chunks: ${m.total_chunks || 20}`,
          `Status: ${m.status || 'ready'}`
        ],
        sentiment: 'Productive',
        nextMilestone: 'Production Ready'
      },
      actionItems: [
        { id: 'a1', task: 'Process RAG query against meeting namespace', owner: 'User', dueDate: 'Today', priority: 'High', completed: false }
      ],
      transcript: [
        { id: 't1', speaker: 'Speaker 1', time: '00:10', text: `Loaded session ${m.title} from Supabase database.` }
      ]
    });
  };

  return (
    <section id="demo" className="py-20 lg:py-28 bg-zinc-950 text-white relative border-t border-zinc-900">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        
        {/* Section Header */}
        <div className="text-center max-w-3xl mx-auto space-y-4 mb-14">
          <div className="inline-flex items-center gap-1.5 px-3 py-1 rounded-full bg-amber-500/10 border border-amber-500/20 text-amber-400 text-xs font-semibold uppercase tracking-wider">
            <Sparkles className="w-3.5 h-3.5" /> Interactive Playground
          </div>
          <h2 className="text-3xl sm:text-5xl font-extrabold text-white tracking-tight">
            Try Database AI Meeting Analysis
          </h2>
          <p className="text-zinc-400 text-base sm:text-lg">
            Inspect real meetings stored inside Supabase DB and see how Claude AI structures transcript notes and action items.
          </p>
        </div>

        {/* Demo Playground Container */}
        <div className="bg-zinc-900/80 border border-zinc-800 rounded-3xl p-4 sm:p-8 shadow-2xl backdrop-blur-xl">
          
          {/* Sample Meeting Selector Pills */}
          <div className="flex flex-wrap items-center gap-3 mb-6 pb-4 border-b border-zinc-800">
            <span className="text-xs font-semibold text-zinc-400 uppercase tracking-wider mr-2">Supabase DB Meetings:</span>
            {meetings.length === 0 ? (
              <span className="text-xs text-zinc-500 font-mono">Loading from database...</span>
            ) : (
              meetings.map((m) => (
                <button
                  key={m.id}
                  onClick={() => handleSelectDbMeeting(m)}
                  className={`px-3.5 py-1.5 rounded-xl text-xs font-medium transition-all cursor-pointer flex items-center gap-2 ${
                    selectedMeeting?.id === m.id
                      ? 'bg-indigo-600 text-white shadow-md shadow-indigo-600/30'
                      : 'bg-zinc-800 text-zinc-300 hover:bg-zinc-700 hover:text-white'
                  }`}
                >
                  <span className="w-2 h-2 rounded-full bg-emerald-400"></span>
                  {m.title}
                </button>
              ))
            )}
          </div>

          {/* Playground Main Grid */}
          {selectedMeeting && (
            <div className="grid grid-cols-1 lg:grid-cols-12 gap-6">
              
              {/* Left Box: Meeting Metadata & Player Simulation */}
              <div className="lg:col-span-5 space-y-4 bg-zinc-950/80 p-5 rounded-2xl border border-zinc-800/80">
                <div className="flex items-center justify-between">
                  <span className="text-[10px] font-mono text-indigo-400 uppercase tracking-wider font-semibold">
                    {selectedMeeting.category}
                  </span>
                  <span className="text-xs text-zinc-400">⏱️ {selectedMeeting.duration}</span>
                </div>

                <h3 className="text-lg font-bold text-white tracking-tight leading-snug">
                  {selectedMeeting.title}
                </h3>
                <p className="text-xs text-zinc-400 font-mono">Recorded: {selectedMeeting.date}</p>

                {/* Audio Waveform Simulation Bar */}
                <div className="p-4 rounded-xl bg-zinc-900 border border-zinc-800 space-y-3">
                  <div className="flex items-center justify-between">
                    <button
                      onClick={() => setIsPlaying(!isPlaying)}
                      className="w-10 h-10 rounded-xl bg-indigo-600 hover:bg-indigo-500 text-white flex items-center justify-center shadow-lg transition-all cursor-pointer"
                    >
                      {isPlaying ? <Pause className="w-4 h-4" /> : <Play className="w-4 h-4 ml-0.5" />}
                    </button>
                    <div className="flex items-center gap-1 flex-1 mx-4 h-6">
                      {[40, 70, 30, 90, 50, 80, 20, 60, 100, 45, 75, 35, 85, 55, 65, 25, 95, 40, 70].map((h, i) => (
                        <div
                          key={i}
                          style={{ height: `${h}%` }}
                          className={`w-1 rounded-full transition-colors ${
                            isPlaying ? 'bg-indigo-400 animate-pulse' : 'bg-zinc-700'
                          }`}
                        />
                      ))}
                    </div>
                    <span className="text-[11px] font-mono text-zinc-400">04:12</span>
                  </div>
                </div>

                <div className="pt-2">
                  <button
                    onClick={() => navigateTo('auth', 'signup')}
                    className="w-full py-3 px-4 rounded-xl text-xs font-semibold text-white bg-indigo-600 hover:bg-indigo-500 shadow-md transition-all flex items-center justify-center gap-2 cursor-pointer"
                  >
                    Get Started Free <ArrowRight className="w-4 h-4" />
                  </button>
                </div>
              </div>

              {/* Right Box: Tabbed Intelligence Output */}
              <div className="lg:col-span-7 bg-zinc-950/80 p-5 rounded-2xl border border-zinc-800/80 flex flex-col justify-between">
                
                <div>
                  {/* Tab Controls */}
                  <div className="flex items-center gap-2 mb-4 pb-3 border-b border-zinc-800">
                    <button
                      onClick={() => setActiveTab('summary')}
                      className={`px-3 py-1.5 rounded-lg text-xs font-medium transition-colors flex items-center gap-1.5 ${
                        activeTab === 'summary' ? 'bg-zinc-800 text-white' : 'text-zinc-400 hover:text-white'
                      }`}
                    >
                      <FileText className="w-3.5 h-3.5 text-indigo-400" /> Summary
                    </button>
                    <button
                      onClick={() => setActiveTab('actions')}
                      className={`px-3 py-1.5 rounded-lg text-xs font-medium transition-colors flex items-center gap-1.5 ${
                        activeTab === 'actions' ? 'bg-zinc-800 text-white' : 'text-zinc-400 hover:text-white'
                      }`}
                    >
                      <CheckSquare className="w-3.5 h-3.5 text-emerald-400" /> Action Items ({selectedMeeting.actionItems.length})
                    </button>
                    <button
                      onClick={() => setActiveTab('transcript')}
                      className={`px-3 py-1.5 rounded-lg text-xs font-medium transition-colors flex items-center gap-1.5 ${
                        activeTab === 'transcript' ? 'bg-zinc-800 text-white' : 'text-zinc-400 hover:text-white'
                      }`}
                    >
                      <MessageSquare className="w-3.5 h-3.5 text-amber-400" /> Chunks
                    </button>
                  </div>

                  {/* Tab Contents */}
                  {activeTab === 'summary' && (
                    <div className="space-y-4">
                      <div className="p-3.5 rounded-xl bg-zinc-900/90 border border-zinc-800/80 space-y-1">
                        <span className="text-[10px] font-semibold text-indigo-400 uppercase tracking-wider">Executive Overview</span>
                        <p className="text-xs text-zinc-300 leading-relaxed">{selectedMeeting.summary.overview}</p>
                      </div>
                      <div className="space-y-2">
                        <span className="text-[10px] font-semibold text-zinc-400 uppercase tracking-wider">Key Takeaways</span>
                        {selectedMeeting.summary.keyTakeaways.map((tk, idx) => (
                          <div key={idx} className="flex items-start gap-2 text-xs text-zinc-300">
                            <span className="text-emerald-400">✓</span>
                            <span>{tk}</span>
                          </div>
                        ))}
                      </div>
                    </div>
                  )}

                  {activeTab === 'actions' && (
                    <div className="space-y-2">
                      {selectedMeeting.actionItems.map((act) => (
                        <div key={act.id} className="p-3 rounded-xl bg-zinc-900 border border-zinc-800 flex items-center justify-between text-xs">
                          <div>
                            <div className="font-medium text-white">{act.task}</div>
                            <div className="text-[10px] text-zinc-400 mt-0.5">Assigned to: {act.owner}</div>
                          </div>
                          <span className="px-2 py-0.5 rounded text-[10px] bg-rose-500/10 text-rose-400 border border-rose-500/20 font-mono">
                            {act.priority}
                          </span>
                        </div>
                      ))}
                    </div>
                  )}

                  {activeTab === 'transcript' && (
                    <div className="space-y-2.5">
                      {selectedMeeting.transcript.map((tr) => (
                        <div key={tr.id} className="p-3 rounded-xl bg-zinc-900/60 border border-zinc-800 text-xs space-y-1">
                          <div className="flex items-center justify-between text-[10px] text-zinc-400">
                            <span className="font-semibold text-indigo-400">{tr.speaker}</span>
                            <span className="font-mono">{tr.time}</span>
                          </div>
                          <p className="text-zinc-300">{tr.text}</p>
                        </div>
                      ))}
                    </div>
                  )}
                </div>

              </div>

            </div>
          )}

        </div>
      </div>
    </section>
  );
}
