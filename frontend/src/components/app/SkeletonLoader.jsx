import React from 'react';

export function SidebarSkeleton() {
  return (
    <div className="space-y-3 p-2 animate-pulse">
      {[1, 2, 3, 4, 5].map((i) => (
        <div key={i} className="p-3 rounded-xl bg-zinc-900 border border-zinc-800/60 space-y-2">
          <div className="h-3.5 bg-zinc-800 rounded-md w-3/4"></div>
          <div className="h-2.5 bg-zinc-850 rounded-md w-1/2"></div>
        </div>
      ))}
    </div>
  );
}

export function HeaderSkeleton() {
  return (
    <div className="p-4 border-b border-zinc-800/80 bg-zinc-950 animate-pulse space-y-3">
      <div className="flex items-center justify-between">
        <div className="space-y-2">
          <div className="h-5 bg-zinc-800 rounded-md w-64"></div>
          <div className="h-3 bg-zinc-850 rounded-md w-40"></div>
        </div>
        <div className="flex gap-2">
          <div className="h-8 w-24 bg-zinc-900 rounded-xl"></div>
          <div className="h-8 w-24 bg-indigo-900/40 rounded-xl"></div>
        </div>
      </div>
    </div>
  );
}

export function ChatSkeleton() {
  return (
    <div className="p-6 space-y-6 animate-pulse max-w-4xl mx-auto">
      {/* User message skeleton */}
      <div className="flex justify-end">
        <div className="bg-zinc-800/80 rounded-2xl p-4 w-2/3 space-y-2">
          <div className="h-3.5 bg-zinc-700 rounded w-full"></div>
          <div className="h-3.5 bg-zinc-700 rounded w-4/5"></div>
        </div>
      </div>

      {/* AI message skeleton */}
      <div className="flex items-start gap-3">
        <div className="w-8 h-8 rounded-lg bg-indigo-600 shrink-0"></div>
        <div className="bg-zinc-900 border border-zinc-800 rounded-2xl p-5 w-3/4 space-y-3">
          <div className="h-4 bg-zinc-800 rounded w-1/3"></div>
          <div className="h-3.5 bg-zinc-850 rounded w-full"></div>
          <div className="h-3.5 bg-zinc-850 rounded w-5/6"></div>
          <div className="h-3.5 bg-zinc-850 rounded w-2/3"></div>
        </div>
      </div>
    </div>
  );
}

export function SummarySkeleton() {
  return (
    <div className="max-w-4xl mx-auto p-6 space-y-6 animate-pulse">
      <div className="p-6 rounded-2xl bg-zinc-900 border border-zinc-800 space-y-3">
        <div className="h-4 bg-indigo-900/50 rounded w-1/4"></div>
        <div className="h-3.5 bg-zinc-800 rounded w-full"></div>
        <div className="h-3.5 bg-zinc-800 rounded w-5/6"></div>
      </div>
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        <div className="p-5 rounded-2xl bg-zinc-900 border border-zinc-800 space-y-2">
          <div className="h-3.5 bg-zinc-800 rounded w-1/2"></div>
          <div className="h-3 bg-zinc-850 rounded w-3/4"></div>
        </div>
        <div className="p-5 rounded-2xl bg-zinc-900 border border-zinc-800 space-y-2">
          <div className="h-3.5 bg-zinc-800 rounded w-1/2"></div>
          <div className="h-3 bg-zinc-850 rounded w-3/4"></div>
        </div>
      </div>
    </div>
  );
}
