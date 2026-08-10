import React from 'react';

export function GridPatternBackground() {
  return (
    <div className="absolute inset-0 overflow-hidden pointer-events-none opacity-40 dark:opacity-40 light:opacity-10">
      <svg
        className="w-full h-full"
        width="100%"
        height="100%"
        xmlns="http://www.w3.org/2000/svg"
      >
        <defs>
          <pattern
            id="grid-pattern-svg"
            width="40"
            height="40"
            patternUnits="userSpaceOnUse"
          >
            <path
              d="M 40 0 L 0 0 0 40"
              fill="none"
              stroke="currentColor"
              strokeWidth="1"
              className="text-zinc-800 dark:text-zinc-800/60 light:text-zinc-300"
            />
            <circle cx="40" cy="40" r="1.5" className="fill-indigo-500/40" />
          </pattern>
          <linearGradient id="grid-fade" x1="0%" y1="0%" x2="0%" y2="100%">
            <stop offset="0%" stopColor="#fff" stopOpacity="1" />
            <stop offset="80%" stopColor="#fff" stopOpacity="0.3" />
            <stop offset="100%" stopColor="#fff" stopOpacity="0" />
          </linearGradient>
          <mask id="grid-mask">
            <rect width="100%" height="100%" fill="url(#grid-fade)" />
          </mask>
        </defs>
        <rect
          width="100%"
          height="100%"
          fill="url(#grid-pattern-svg)"
          mask="url(#grid-mask)"
        />
      </svg>
    </div>
  );
}

export function GlowingHeroBg() {
  return (
    <div className="absolute top-0 left-1/2 -translate-x-1/2 w-full max-w-7xl h-[600px] pointer-events-none overflow-hidden -z-10">
      <svg
        viewBox="0 0 1000 600"
        fill="none"
        xmlns="http://www.w3.org/2000/svg"
        className="w-full h-full opacity-60 dark:opacity-60 light:opacity-20 blur-3xl"
      >
        <circle cx="500" cy="180" r="280" fill="url(#hero-glow-grad1)" />
        <circle cx="750" cy="220" r="220" fill="url(#hero-glow-grad2)" />
        <circle cx="250" cy="240" r="200" fill="url(#hero-glow-grad3)" />
        <defs>
          <radialGradient
            id="hero-glow-grad1"
            cx="0"
            cy="0"
            r="1"
            gradientUnits="userSpaceOnUse"
            gradientTransform="translate(500 180) rotate(90) scale(280)"
          >
            <stop stopColor="#6366f1" stopOpacity="0.45" />
            <stop offset="1" stopColor="#6366f1" stopOpacity="0" />
          </radialGradient>
          <radialGradient
            id="hero-glow-grad2"
            cx="0"
            cy="0"
            r="1"
            gradientUnits="userSpaceOnUse"
            gradientTransform="translate(750 220) rotate(90) scale(220)"
          >
            <stop stopColor="#a855f7" stopOpacity="0.35" />
            <stop offset="1" stopColor="#a855f7" stopOpacity="0" />
          </radialGradient>
          <radialGradient
            id="hero-glow-grad3"
            cx="0"
            cy="0"
            r="1"
            gradientUnits="userSpaceOnUse"
            gradientTransform="translate(250 240) rotate(90) scale(200)"
          >
            <stop stopColor="#10b981" stopOpacity="0.3" />
            <stop offset="1" stopColor="#10b981" stopOpacity="0" />
          </radialGradient>
        </defs>
      </svg>
    </div>
  );
}

export function WaveMeshBackground() {
  return (
    <div className="absolute inset-0 pointer-events-none opacity-25 overflow-hidden">
      <svg
        viewBox="0 0 1440 400"
        fill="none"
        xmlns="http://www.w3.org/2000/svg"
        className="w-full h-full preserve-3d"
      >
        <path
          d="M0,160 C320,300 420,0 720,120 C1020,240 1120,40 1440,200 L1440,400 L0,400 Z"
          fill="url(#wave-grad-1)"
        />
        <path
          d="M0,220 C240,100 480,280 720,180 C960,80 1200,260 1440,140 L1440,400 L0,400 Z"
          fill="url(#wave-grad-2)"
        />
        <defs>
          <linearGradient id="wave-grad-1" x1="0%" y1="0%" x2="100%" y2="0%">
            <stop offset="0%" stopColor="#4f46e5" stopOpacity="0.15" />
            <stop offset="50%" stopColor="#9333ea" stopOpacity="0.2" />
            <stop offset="100%" stopColor="#06b6d4" stopOpacity="0.1" />
          </linearGradient>
          <linearGradient id="wave-grad-2" x1="0%" y1="0%" x2="100%" y2="0%">
            <stop offset="0%" stopColor="#10b981" stopOpacity="0.1" />
            <stop offset="50%" stopColor="#6366f1" stopOpacity="0.18" />
            <stop offset="100%" stopColor="#ec4899" stopOpacity="0.12" />
          </linearGradient>
        </defs>
      </svg>
    </div>
  );
}
