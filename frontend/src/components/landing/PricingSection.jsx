import React, { useState } from 'react';
import { Check, ArrowRight } from 'lucide-react';
import { useAuth } from '../../context/AuthContext';
import { motion } from 'framer-motion';

const PRICING_PLANS = [
  {
    name: 'Starter',
    price: '$0',
    period: 'forever free',
    description: 'Perfect for freelancers & small teams capturing team syncs.',
    features: [
      'Up to 10 hours of meeting transcription/mo',
      'AI Executive Summaries & Key Points',
      'Basic Action Item Detection',
      'Export to Markdown & Plain Text',
      'Standard Dark & Light UI Theme'
    ],
    cta: 'Start Free Today',
    popular: false
  },
  {
    name: 'Pro Team',
    price: '$19',
    period: 'per user / month',
    description: 'Empower high-velocity product & engineering teams.',
    features: [
      'Unlimited meeting transcription hours',
      'Claude 3.5 Sonnet AI Chat & Intelligence',
      'Automated Speaker Diarization & Analytics',
      'Direct Jira, Linear, Slack & Notion Sync',
      'Custom Audio/Video Upload (MP3, MP4, WAV)',
      'Priority E2E Encrypted Processing'
    ],
    cta: 'Start 14-Day Free Trial',
    popular: true
  },
  {
    name: 'Enterprise',
    price: 'Custom',
    period: 'tailored annual billing',
    description: 'Built for enterprise security, HIPAA & SOC2 compliance.',
    features: [
      'Dedicated GPU Inference Nodes (<150ms)',
      'Custom On-Premises or Private Cloud Deploy',
      'SOC2 Type II, HIPAA & Single Sign-On (SAML/Okta)',
      'Unlimited Workspace Team Members',
      'Dedicated Account Manager & 24/7 SLA'
    ],
    cta: 'Contact Sales',
    popular: false
  }
];

export default function PricingSection() {
  const { navigateTo } = useAuth();
  const [billingCycle, setBillingCycle] = useState('monthly'); // 'monthly' or 'annual'

  return (
    <section id="pricing" className="py-20 lg:py-28 bg-zinc-950 text-white relative border-t border-zinc-900">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        
        {/* Section Header */}
        <div className="text-center max-w-3xl mx-auto space-y-4 mb-12">
          <div className="inline-flex items-center gap-1.5 px-3 py-1 rounded-full bg-indigo-500/10 border border-indigo-500/20 text-indigo-400 text-xs font-semibold uppercase tracking-wider">
            Predictable Pricing
          </div>
          <h2 className="text-3xl sm:text-5xl font-extrabold tracking-tight">
            Transparent Plans for Every Stage
          </h2>
          <p className="text-zinc-400 text-base sm:text-lg">
            Start free, upgrade as your team grows. No hidden transcription fees.
          </p>

          {/* Billing Cycle Switch */}
          <div className="pt-4 flex items-center justify-center gap-3">
            <span className={`text-sm font-medium ${billingCycle === 'monthly' ? 'text-white' : 'text-zinc-500'}`}>
              Monthly Billing
            </span>
            <button
              onClick={() => setBillingCycle(billingCycle === 'monthly' ? 'annual' : 'monthly')}
              className="w-12 h-6 rounded-full bg-zinc-800 p-1 relative border border-zinc-700 transition-colors cursor-pointer"
            >
              <div
                className={`w-4 h-4 rounded-full bg-indigo-500 transition-transform ${
                  billingCycle === 'annual' ? 'translate-x-6' : 'translate-x-0'
                }`}
              />
            </button>
            <span className={`text-sm font-medium flex items-center gap-1.5 ${billingCycle === 'annual' ? 'text-white' : 'text-zinc-500'}`}>
              Annual Billing
              <span className="px-2 py-0.5 rounded-full text-[10px] font-bold bg-emerald-500/10 text-emerald-400 border border-emerald-500/20">
                Save 20%
              </span>
            </span>
          </div>
        </div>

        {/* Pricing Cards Grid */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-8 items-stretch">
          {PRICING_PLANS.map((plan, idx) => (
            <motion.div
              key={idx}
              initial={{ opacity: 0, y: 20 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true }}
              transition={{ duration: 0.5, delay: idx * 0.15 }}
              className={`rounded-3xl p-8 flex flex-col justify-between relative transition-all ${
                plan.popular
                  ? 'bg-zinc-900 border-2 border-indigo-500 shadow-2xl shadow-indigo-500/20 scale-105 z-10'
                  : 'bg-zinc-900/60 border border-zinc-800 hover:border-zinc-700'
              }`}
            >
              {plan.popular && (
                <div className="absolute -top-3.5 left-1/2 -translate-x-1/2 px-3 py-1 rounded-full bg-gradient-to-r from-indigo-500 to-purple-500 text-white text-[11px] font-bold uppercase tracking-wider shadow-lg">
                  Most Popular Team Choice
                </div>
              )}

              <div className="space-y-6">
                <div>
                  <h3 className="text-xl font-bold text-white">{plan.name}</h3>
                  <p className="text-xs text-zinc-400 mt-1 min-h-[32px]">{plan.description}</p>
                </div>

                <div className="flex items-baseline gap-1">
                  <span className="text-4xl sm:text-5xl font-extrabold text-white">
                    {billingCycle === 'annual' && plan.price.startsWith('$') 
                      ? `$${Math.round(parseInt(plan.price.replace('$', '')) * 0.8)}`
                      : plan.price
                    }
                  </span>
                  <span className="text-xs text-zinc-400">{plan.period}</span>
                </div>

                <ul className="space-y-3 pt-2 text-xs text-zinc-300">
                  {plan.features.map((f, i) => (
                    <li key={i} className="flex items-start gap-2.5">
                      <Check className="w-4 h-4 text-emerald-400 shrink-0 mt-0.5" />
                      <span>{f}</span>
                    </li>
                  ))}
                </ul>
              </div>

              <div className="pt-8">
                <button
                  onClick={() => navigateTo('auth', 'signup')}
                  className={`w-full py-3 px-4 rounded-xl text-sm font-semibold transition-all cursor-pointer flex items-center justify-center gap-2 ${
                    plan.popular
                      ? 'bg-indigo-600 hover:bg-indigo-500 text-white shadow-lg shadow-indigo-600/30'
                      : 'bg-zinc-800 hover:bg-zinc-700 text-zinc-100 border border-zinc-700'
                  }`}
                >
                  {plan.cta}
                  <ArrowRight className="w-4 h-4" />
                </button>
              </div>
            </motion.div>
          ))}
        </div>

      </div>
    </section>
  );
}
