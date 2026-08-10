import React, { useState } from 'react';
import { Settings, X, Bot, Shield, Bell, Key } from 'lucide-react';

export default function SettingsModal({ isOpen, onClose }) {
  const [model, setModel] = useState('Claude 3.5 Sonnet');
  const [speechModel, setSpeechModel] = useState('Whisper Large v3');
  const [jiraSync, setJiraSync] = useState(true);

  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/80 backdrop-blur-sm">
      <div className="bg-zinc-900 border border-zinc-800 rounded-3xl p-6 sm:p-8 max-w-lg w-full shadow-2xl relative text-zinc-200">
        
        <button
          onClick={onClose}
          className="absolute top-5 right-5 p-1.5 rounded-lg text-zinc-400 hover:text-white hover:bg-zinc-800"
        >
          <X className="w-5 h-5" />
        </button>

        <div className="flex items-center gap-2 mb-6">
          <Settings className="w-5 h-5 text-indigo-400" />
          <h3 className="text-xl font-bold text-white">Workspace Settings</h3>
        </div>

        <div className="space-y-4 text-xs">
          <div>
            <label className="block text-zinc-400 font-medium mb-1">AI Intelligence Model</label>
            <select
              value={model}
              onChange={(e) => setModel(e.target.value)}
              className="w-full p-2.5 rounded-xl bg-zinc-950 border border-zinc-800 text-white focus:outline-none focus:border-indigo-500"
            >
              <option value="Claude 3.5 Sonnet">Claude 3.5 Sonnet (Default High Precision)</option>
              <option value="Claude 3 Opus">Claude 3 Opus (Extended Reasoning)</option>
              <option value="Claude 3.5 Haiku">Claude 3.5 Haiku (Fast Speed)</option>
            </select>
          </div>

          <div>
            <label className="block text-zinc-400 font-medium mb-1">Speech Transcription Engine</label>
            <select
              value={speechModel}
              onChange={(e) => setSpeechModel(e.target.value)}
              className="w-full p-2.5 rounded-xl bg-zinc-950 border border-zinc-800 text-white focus:outline-none focus:border-indigo-500"
            >
              <option value="Whisper Large v3">Whisper Large v3 (98.4% Accuracy)</option>
              <option value="Whisper Realtime Latency Engine">Whisper Realtime (&lt;150ms Latency)</option>
            </select>
          </div>

          <div className="p-3 rounded-xl bg-zinc-950 border border-zinc-800 flex items-center justify-between">
            <div>
              <div className="font-semibold text-white">Auto-Sync Tasks to Jira / Slack</div>
              <div className="text-zinc-500 text-[10px]">Automatically dispatch action items on meeting close</div>
            </div>
            <input
              type="checkbox"
              checked={jiraSync}
              onChange={(e) => setJiraSync(e.target.checked)}
              className="w-4 h-4 accent-indigo-500 rounded cursor-pointer"
            />
          </div>
        </div>

        <div className="pt-6 flex justify-end gap-2">
          <button
            onClick={onClose}
            className="px-4 py-2 rounded-xl bg-zinc-800 hover:bg-zinc-700 text-xs font-semibold text-zinc-200"
          >
            Cancel
          </button>
          <button
            onClick={() => { alert('Settings saved successfully!'); onClose(); }}
            className="px-4 py-2 rounded-xl bg-indigo-600 hover:bg-indigo-500 text-xs font-semibold text-white shadow-md"
          >
            Save Preferences
          </button>
        </div>

      </div>
    </div>
  );
}
