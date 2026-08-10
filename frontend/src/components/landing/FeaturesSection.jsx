import React from 'react';
import { 
  Mic, Sparkles, CheckSquare, ShieldCheck, Search, Moon, 
  ArrowUpRight 
} from 'lucide-react';
import { motion } from 'framer-motion';

const FEATURES_LIST = [
  {
    icon: 'Mic',
    title: 'Whisper-Large-v3 Speech Diarization',
    description: 'High-precision multi-speaker speech-to-text recognition with sub-300ms audio streaming latency.',
    badge: 'Real-Time Audio'
  },
  {
    icon: 'Sparkles',
    title: 'Claude 3.5 Executive Summarizer',
    description: 'Automated executive meeting summaries, key takeaways, and structured transcript analysis.',
    badge: 'AI Intelligence'
  },
  {
    icon: 'CheckSquare',
    title: 'Automated Checkable Action Items',
    description: 'Extract tasks with assignees and due dates, then sync directly to Jira, Linear, and Slack.',
    badge: 'Auto-Sync'
  },
  {
    icon: 'ShieldCheck',
    title: 'Supabase DB & Pinecone RAG',
    description: 'Secure Supabase database storage with Pinecone vector RAG search across meeting transcripts.',
    badge: 'Vector RAG'
  },
  {
    icon: 'Search',
    title: 'Semantic Cross-Meeting Search',
    description: 'Query questions across your historical meeting transcripts with vector embeddings.',
    badge: 'Pinecone Vector'
  },
  {
    icon: 'Moon',
    title: 'Obsidian Dark UI Theme',
    description: 'High readability obsidian interface tailored for engineering and product teams.',
    badge: 'Dark Mode'
  }
];

const iconMap = {
  Mic: Mic,
  Sparkles: Sparkles,
  CheckSquare: CheckSquare,
  ShieldCheck: ShieldCheck,
  Search: Search,
  Moon: Moon
};

export default function FeaturesSection() {
  return (
    <section id="features" className="py-20 lg:py-28 bg-zinc-950 text-white relative">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        
        <div className="text-center max-w-3xl mx-auto space-y-4 mb-16">
          <div className="inline-flex items-center gap-1.5 px-3 py-1 rounded-full bg-indigo-500/10 border border-indigo-500/20 text-indigo-400 text-xs font-semibold uppercase tracking-wider">
            <Sparkles className="w-3.5 h-3.5" /> Platform Capabilities
          </div>
          <h2 className="text-3xl sm:text-5xl font-extrabold tracking-tight text-white">
            Engineered for High-Output Product Teams
          </h2>
          <p className="text-zinc-400 text-base sm:text-lg">
            Everything you need to turn spoken meeting audio into structured database records and actionable engineering workflows.
          </p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 lg:gap-8">
          {FEATURES_LIST.map((feature, idx) => {
            const IconComponent = iconMap[feature.icon] || Sparkles;
            return (
              <motion.div
                key={feature.title}
                initial={{ opacity: 0, y: 20 }}
                whileInView={{ opacity: 1, y: 0 }}
                viewport={{ once: true }}
                transition={{ duration: 0.4, delay: idx * 0.08 }}
                className="p-6 rounded-3xl bg-zinc-900/70 border border-zinc-800/80 hover:border-indigo-500/40 transition-all hover:shadow-2xl group flex flex-col justify-between"
              >
                <div className="space-y-4">
                  <div className="flex items-center justify-between">
                    <div className="w-12 h-12 rounded-2xl bg-indigo-500/10 border border-indigo-500/20 text-indigo-400 flex items-center justify-center group-hover:scale-105 transition-transform">
                      <IconComponent className="w-6 h-6" />
                    </div>
                    <span className="text-[10px] font-mono font-semibold px-2.5 py-1 rounded-full bg-zinc-800 text-zinc-300 border border-zinc-700">
                      {feature.badge}
                    </span>
                  </div>

                  <h3 className="text-lg font-bold text-white group-hover:text-indigo-300 transition-colors">
                    {feature.title}
                  </h3>
                  <p className="text-xs text-zinc-400 leading-relaxed">
                    {feature.description}
                  </p>
                </div>

                <div className="pt-6 mt-4 border-t border-zinc-800/60 flex items-center text-xs font-semibold text-indigo-400 group-hover:text-indigo-300">
                  <span>Explore Feature</span>
                  <ArrowUpRight className="w-4 h-4 ml-1 group-hover:translate-x-0.5 group-hover:-translate-y-0.5 transition-transform" />
                </div>
              </motion.div>
            );
          })}
        </div>

      </div>
    </section>
  );
}
