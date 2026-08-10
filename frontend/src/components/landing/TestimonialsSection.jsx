import React from 'react';
import { Star } from 'lucide-react';
import { motion } from 'framer-motion';

const TESTIMONIALS_LIST = [
  {
    quote: "This AI Meeting Assistant changed how our engineering team operates. We save 4+ hours every week by letting the Claude interface generate action items directly into Jira.",
    author: "Elena Rostova",
    title: "VP of Engineering at CloudScale",
    avatar: "https://images.unsplash.com/photo-1573496359142-b8d87734a5a2?auto=format&fit=crop&q=80&w=150"
  },
  {
    quote: "The dark obsidian interface is pure perfection. It looks and feels as fast and clean as Anthropic's Claude UI. Transcripts are spot-on even with complex technical jargon.",
    author: "Marcus Chen",
    title: "Lead Architect at DevPulse",
    avatar: "https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?auto=format&fit=crop&q=80&w=150"
  },
  {
    quote: "Searching across 6 months of executive leadership meetings with semantic vector search saved us during our annual audit. Essential tool for remote leadership.",
    author: "Sarah Jenkins",
    title: "Chief Product Officer at Vantage AI",
    avatar: "https://images.unsplash.com/photo-1580489944761-15a19d654956?auto=format&fit=crop&q=80&w=150"
  }
];

export default function TestimonialsSection() {
  return (
    <section id="testimonials" className="py-20 lg:py-28 bg-zinc-950 text-white relative border-t border-zinc-900">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        
        <div className="text-center max-w-3xl mx-auto space-y-4 mb-16">
          <div className="inline-flex items-center gap-1.5 px-3 py-1 rounded-full bg-emerald-500/10 border border-emerald-500/20 text-emerald-400 text-xs font-semibold uppercase tracking-wider">
            Loved by Product & Engineering Leaders
          </div>
          <h2 className="text-3xl sm:text-5xl font-extrabold tracking-tight">
            Trusted by Teams Shipping at Scale
          </h2>
          <p className="text-zinc-400 text-base sm:text-lg">
            See how top technology companies use MeetingSense AI to eliminate meeting fatigue and automate task assignment.
          </p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          {TESTIMONIALS_LIST.map((t, idx) => (
            <motion.div
              key={idx}
              initial={{ opacity: 0, y: 20 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true }}
              transition={{ duration: 0.5, delay: idx * 0.15 }}
              className="bg-zinc-900/60 border border-zinc-800 p-6 rounded-2xl flex flex-col justify-between space-y-6 relative hover:border-zinc-700 transition-all"
            >
              <div className="space-y-4">
                <div className="flex items-center gap-1 text-amber-400">
                  {Array.from({ length: 5 }).map((_, i) => (
                    <Star key={i} className="w-4 h-4 fill-amber-400" />
                  ))}
                </div>
                <p className="text-zinc-300 text-sm leading-relaxed italic">
                  "{t.quote}"
                </p>
              </div>

              <div className="flex items-center gap-3 pt-4 border-t border-zinc-800/80">
                <img src={t.avatar} alt={t.author} className="w-10 h-10 rounded-full object-cover border border-zinc-700" />
                <div>
                  <h4 className="font-bold text-white text-sm">{t.author}</h4>
                  <p className="text-xs text-zinc-400">{t.title}</p>
                </div>
              </div>
            </motion.div>
          ))}
        </div>

      </div>
    </section>
  );
}
