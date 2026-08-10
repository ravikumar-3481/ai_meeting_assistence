import React from 'react';
import { 
  Plus, MessageSquare, UploadCloud, 
  Settings, LogOut, ChevronLeft, ChevronRight, 
  Bot 
} from 'lucide-react';
import { useAuth } from '../../context/AuthContext';
import ThemeToggle from '../common/ThemeToggle';

export default function ClaudeSidebar({ 
  meetings = [],
  selectedMeeting, 
  onSelectMeeting, 
  onOpenUpload, 
  onOpenSettings,
  isCollapsed,
  onToggleCollapse
}) {
  const { user, logout } = useAuth();

  return (
    <aside
      className={`bg-zinc-950 dark:bg-zinc-950 light:bg-zinc-100 border-r border-zinc-800/80 light:border-zinc-300 flex flex-col justify-between transition-all duration-300 relative z-20 ${
        isCollapsed ? 'w-16' : 'w-72'
      }`}
    >
      {/* Top Brand & Collapse Toggle */}
      <div className="p-3 border-b border-zinc-800/80 flex items-center justify-between">
        {!isCollapsed && (
          <div className="flex items-center gap-2.5 px-2">
            <div className="w-8 h-8 rounded-lg bg-gradient-to-br from-indigo-500 to-emerald-500 p-[1px]">
              <div className="w-full h-full bg-zinc-950 rounded-[7px] flex items-center justify-center">
                <Bot className="w-4 h-4 text-indigo-400" />
              </div>
            </div>
            <div>
              <span className="font-bold text-sm text-zinc-100 dark:text-zinc-100 light:text-zinc-900 tracking-tight block">
                MeetingSense
              </span>
              <span className="text-[9px] font-mono text-indigo-400 block">DB CONNECTED</span>
            </div>
          </div>
        )}

        <button
          onClick={onToggleCollapse}
          className="p-1.5 rounded-lg text-zinc-400 hover:text-white hover:bg-zinc-800/60 transition-colors mx-auto"
          title={isCollapsed ? 'Expand Sidebar' : 'Collapse Sidebar'}
        >
          {isCollapsed ? <ChevronRight className="w-4 h-4" /> : <ChevronLeft className="w-4 h-4" />}
        </button>
      </div>

      {/* Main Action Buttons & History List */}
      <div className="flex-1 overflow-y-auto p-3 space-y-4">
        
        {/* New Session & Upload Buttons */}
        <div className="space-y-2">
          <button
            onClick={onOpenUpload}
            className={`w-full py-2.5 px-3 rounded-xl bg-indigo-600 hover:bg-indigo-500 text-white font-semibold text-xs flex items-center justify-center gap-2 shadow-lg shadow-indigo-600/20 transition-all cursor-pointer ${
              isCollapsed ? 'p-2' : ''
            }`}
          >
            <Plus className="w-4 h-4" />
            {!isCollapsed && <span>Process New Meeting</span>}
          </button>

          <button
            onClick={onOpenUpload}
            className={`w-full py-2.5 px-3 rounded-xl bg-zinc-900 hover:bg-zinc-800 text-zinc-300 border border-zinc-800 text-xs font-medium flex items-center justify-center gap-2 transition-all cursor-pointer ${
              isCollapsed ? 'p-2' : ''
            }`}
          >
            <UploadCloud className="w-4 h-4 text-emerald-400" />
            {!isCollapsed && <span>Upload Audio / YouTube</span>}
          </button>
        </div>

        {/* Meeting History List from Database */}
        {!isCollapsed ? (
          <div className="space-y-4 pt-2">
            <div className="text-[11px] font-semibold text-zinc-500 uppercase tracking-wider px-2 flex justify-between items-center">
              <span>Database Meetings ({meetings.length})</span>
            </div>

            {meetings.length === 0 ? (
              <div className="p-3 bg-zinc-900/60 border border-zinc-800/60 rounded-xl text-center">
                <p className="text-xs text-zinc-400">No meetings in database yet.</p>
                <p className="text-[10px] text-zinc-500 mt-1">Click above to ingest YouTube or transcript.</p>
              </div>
            ) : (
              <div className="space-y-1">
                {meetings.map((m) => {
                  const mId = m.id || m.pinecone_namespace;
                  const isActive = selectedMeeting?.id === mId || selectedMeeting?.pinecone_namespace === mId;
                  return (
                    <button
                      key={mId}
                      onClick={() => onSelectMeeting(m)}
                      className={`w-full text-left p-2.5 rounded-xl text-xs transition-all cursor-pointer group flex items-start gap-2.5 ${
                        isActive
                          ? 'bg-zinc-800 text-white border border-indigo-500/40 shadow-inner'
                          : 'text-zinc-400 hover:text-zinc-200 hover:bg-zinc-900/60'
                      }`}
                    >
                      <MessageSquare className={`w-3.5 h-3.5 shrink-0 mt-0.5 ${isActive ? 'text-indigo-400' : 'text-zinc-500 group-hover:text-zinc-300'}`} />
                      <div className="flex-1 truncate">
                        <div className="font-medium truncate text-zinc-200">{m.title || 'Untitled Meeting'}</div>
                        <div className="text-[10px] text-zinc-500 flex items-center gap-2 mt-0.5">
                          <span>{m.created_at ? new Date(m.created_at).toLocaleDateString() : 'Ready'}</span>
                          <span>•</span>
                          <span className="text-indigo-400 uppercase">{m.language || 'EN'}</span>
                        </div>
                      </div>
                    </button>
                  );
                })}
              </div>
            )}
          </div>
        ) : (
          <div className="flex flex-col items-center gap-2 pt-2">
            {meetings.map((m) => {
              const mId = m.id || m.pinecone_namespace;
              const isActive = selectedMeeting?.id === mId || selectedMeeting?.pinecone_namespace === mId;
              return (
                <button
                  key={mId}
                  onClick={() => onSelectMeeting(m)}
                  className={`w-9 h-9 rounded-xl flex items-center justify-center transition-colors ${
                    isActive ? 'bg-indigo-600 text-white' : 'bg-zinc-900 text-zinc-400 hover:bg-zinc-800'
                  }`}
                  title={m.title}
                >
                  <MessageSquare className="w-4 h-4" />
                </button>
              );
            })}
          </div>
        )}

      </div>

      {/* User Profile & Footer Controls */}
      <div className="p-3 border-t border-zinc-800/80 space-y-2">
        <div className="flex items-center justify-between">
          <ThemeToggle />
          {!isCollapsed && (
            <button
              onClick={onOpenSettings}
              className="p-2 rounded-lg text-zinc-400 hover:text-white hover:bg-zinc-800 transition-colors"
              title="Settings"
            >
              <Settings className="w-4 h-4" />
            </button>
          )}
        </div>

        {!isCollapsed ? (
          <div className="p-2 rounded-xl bg-zinc-900 border border-zinc-800/80 flex items-center justify-between">
            <div className="flex items-center gap-2.5 truncate">
              <div className="w-7 h-7 rounded-full bg-gradient-to-tr from-indigo-500 to-emerald-500 flex items-center justify-center text-xs font-bold text-white shrink-0">
                {(user?.name || user?.email || 'U')[0].toUpperCase()}
              </div>
              <div className="truncate">
                <div className="font-semibold text-xs text-zinc-200 truncate">{user?.name || user?.email?.split('@')[0] || 'User'}</div>
                <div className="text-[10px] text-zinc-500 truncate">{user?.email || 'Authenticated DB User'}</div>
              </div>
            </div>
            <button
              onClick={logout}
              className="p-1.5 rounded-lg text-zinc-500 hover:text-rose-400 hover:bg-rose-500/10 transition-colors"
              title="Log Out"
            >
              <LogOut className="w-4 h-4" />
            </button>
          </div>
        ) : (
          <button
            onClick={logout}
            className="w-full p-2 rounded-xl bg-zinc-900 text-zinc-500 hover:text-rose-400 flex items-center justify-center"
            title="Log Out"
          >
            <LogOut className="w-4 h-4" />
          </button>
        )}
      </div>

    </aside>
  );
}
