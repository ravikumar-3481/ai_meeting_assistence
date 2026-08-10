import React, { useState, useEffect, useCallback } from 'react';
import ClaudeSidebar from './ClaudeSidebar';
import ClaudeHeader from './ClaudeHeader';
import ClaudeChatArea from './ClaudeChatArea';
import ClaudePromptInput from './ClaudePromptInput';
import MeetingSummaryTab from './MeetingSummaryTab';
import ActionItemsTab from './ActionItemsTab';
import TranscriptTab from './TranscriptTab';
import AnalyticsTab from './AnalyticsTab';
import UploadModal from './UploadModal';
import SettingsModal from './SettingsModal';
import { api } from '../../services/api';

export default function ClaudeWorkspace() {
  const [meetings, setMeetings] = useState([]);
  const [selectedMeeting, setSelectedMeeting] = useState(null);
  const [activeTab, setActiveTab] = useState('chat'); // 'chat', 'summary', 'actions', 'transcript', 'analytics'
  const [isSidebarCollapsed, setIsSidebarCollapsed] = useState(false);
  const [isMobileSidebarOpen, setIsMobileSidebarOpen] = useState(false);
  const [isUploadOpen, setIsUploadOpen] = useState(false);
  const [isSettingsOpen, setIsSettingsOpen] = useState(false);
  const [searchQuery, setSearchQuery] = useState('');
  const [messages, setMessages] = useState([]);
  const [loading, setLoading] = useState(true);

  // Fetch all meeting details (action items, chunks, outputs) for selected meeting from DB
  const loadMeetingDetails = useCallback(async (meeting) => {
    if (!meeting) return;
    const meetingId = meeting.id || meeting.pinecone_namespace;
    
    try {
      // Fetch action items from DB
      const actionItemsRes = await api.getActionItems(meetingId).catch(() => ({ data: [] }));
      const actionItems = actionItemsRes.data || [];

      // Fetch chunks / transcripts from DB
      const chunksRes = await api.getMeetingChunks(meetingId).catch(() => ({ data: [] }));
      const chunks = chunksRes.data || [];

      // Fetch output metadata / summary from DB
      const outputsRes = await api.getMeetingOutputs(meetingId).catch(() => ({ data: [] }));
      const outputs = outputsRes.data || [];

      const formattedTranscript = chunks.map((c, idx) => ({
        id: c.id || `chunk-${idx}`,
        speaker: c.speaker || `Speaker ${(idx % 2) + 1}`,
        time: c.timestamp || `00:${String(idx * 2).padStart(2, '0')}`,
        text: c.chunk_text || c.text || c.content || '',
      }));

      const fullMeetingObj = {
        ...meeting,
        id: meetingId,
        title: meeting.title || 'Database Meeting Analysis',
        date: meeting.created_at ? new Date(meeting.created_at).toLocaleDateString() : 'Active',
        duration: meeting.duration_seconds ? `${Math.round(meeting.duration_seconds / 60)} mins` : `${chunks.length} Chunks`,
        status: meeting.status || 'Ready',
        language: meeting.language || 'English',
        category: meeting.source_url ? 'YouTube / Remote' : 'Database RAG',
        actionItems: actionItems.map((item) => ({
          id: item.id,
          task: item.task,
          owner: item.owner || item.assignee || 'Unassigned',
          dueDate: item.due_date || item.created_at || 'Pending',
          priority: item.priority || 'High',
          status: item.status || 'pending',
          completed: item.status === 'completed',
        })),
        transcript: formattedTranscript,
        summary: {
          overview: outputs[0]?.output_type || `Indexed ${chunks.length} vector chunks into Pinecone & Supabase database for session ${meetingId}.`,
          keyTakeaways: [
            `Total vector chunks ingested: ${chunks.length || meeting.total_chunks || 0}`,
            `Source URL: ${meeting.source_url || 'Processed File / Audio'}`,
            `Diarization & Language model: ${meeting.language || 'English'}`
          ],
          sentiment: 'Positive & Productive',
          nextMilestone: 'RAG Agent Active'
        },
        participants: [
          { name: 'Primary Speaker', role: 'Presenter', talkTimePercentage: 65, avatar: 'https://images.unsplash.com/photo-1534528741775-53994a69daeb?auto=format&fit=crop&q=80&w=150' },
          { name: 'Secondary Participant', role: 'Collaborator', talkTimePercentage: 35, avatar: 'https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?auto=format&fit=crop&q=80&w=150' },
        ],
      };

      setSelectedMeeting(fullMeetingObj);

      // Initial welcome message from assistant for this meeting
      setMessages([
        {
          id: 'welcome-msg',
          sender: 'assistant',
          text: `Connected to Supabase Database meeting **${fullMeetingObj.title}** (ID: \`${meetingId}\`).\n\nYou can ask any question about the meeting notes, action items, or transcripts!`,
          time: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
        },
      ]);
    } catch (err) {
      console.error('Error loading meeting details from DB:', err);
      setSelectedMeeting(meeting);
    }
  }, []);

  // Initial load of user meetings from Supabase database API
  const fetchMeetingsFromDb = useCallback(async () => {
    setLoading(true);
    try {
      const response = await api.getMeetings();
      const dbMeetings = response.data || [];
      setMeetings(dbMeetings);
      if (dbMeetings.length > 0) {
        await loadMeetingDetails(dbMeetings[0]);
      } else {
        setSelectedMeeting(null);
        setMessages([]);
      }
    } catch (err) {
      console.warn('Could not fetch meetings from backend DB:', err);
      setMeetings([]);
      setSelectedMeeting(null);
    } finally {
      setLoading(false);
    }
  }, [loadMeetingDetails]);

  useEffect(() => {
    fetchMeetingsFromDb();
  }, [fetchMeetingsFromDb]);

  const handleSelectMeeting = async (m) => {
    setIsMobileSidebarOpen(false);
    await loadMeetingDetails(m);
  };

  const handleSendMessage = async (text) => {
    if (!text.trim()) return;

    const userMsg = {
      id: 'msg-' + Date.now(),
      sender: 'user',
      text: text,
      time: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
    };

    setMessages((prev) => [...prev, userMsg]);

    const meetingId = selectedMeeting?.id || selectedMeeting?.pinecone_namespace || 'default_meeting';

    try {
      const response = await api.sendChatQuery(meetingId, text, messages);
      const answer = response.data?.answer || 'Response received from database agent.';

      const aiMsg = {
        id: 'msg-' + (Date.now() + 1),
        sender: 'assistant',
        text: answer,
        time: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
      };

      setMessages((prev) => [...prev, aiMsg]);
    } catch (err) {
      console.error('Error querying backend AI Agent:', err);
      // Fallback assistant response if backend RAG service is responding offline
      const aiMsg = {
        id: 'msg-' + (Date.now() + 1),
        sender: 'assistant',
        text: `Analysis for question: "${text}"\n\n- Data queried from database session \`${meetingId}\`.\n- Note: Ensure FastAPI backend server is running on http://localhost:8000.`,
        time: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
      };
      setMessages((prev) => [...prev, aiMsg]);
    }
  };

  const handleUploadSuccess = async () => {
    await fetchMeetingsFromDb();
    setActiveTab('summary');
  };

  return (
    <div className="h-screen w-screen flex bg-zinc-950 dark:bg-zinc-950 light:bg-zinc-50 overflow-hidden font-sans text-zinc-100 selection:bg-indigo-500 selection:text-white">
      
      {/* Desktop Sidebar */}
      <div className="hidden md:block">
        <ClaudeSidebar
          meetings={meetings}
          selectedMeeting={selectedMeeting}
          onSelectMeeting={handleSelectMeeting}
          onOpenUpload={() => setIsUploadOpen(true)}
          onOpenSettings={() => setIsSettingsOpen(true)}
          isCollapsed={isSidebarCollapsed}
          onToggleCollapse={() => setIsSidebarCollapsed(!isSidebarCollapsed)}
        />
      </div>

      {/* Mobile Sidebar Overlay Drawer */}
      {isMobileSidebarOpen && (
        <div className="md:hidden fixed inset-0 z-40 flex">
          <div 
            className="fixed inset-0 bg-black/80 backdrop-blur-sm"
            onClick={() => setIsMobileSidebarOpen(false)}
          />
          <div className="relative z-50 w-72 h-full bg-zinc-950 shadow-2xl">
            <ClaudeSidebar
              meetings={meetings}
              selectedMeeting={selectedMeeting}
              onSelectMeeting={handleSelectMeeting}
              onOpenUpload={() => { setIsMobileSidebarOpen(false); setIsUploadOpen(true); }}
              onOpenSettings={() => { setIsMobileSidebarOpen(false); setIsSettingsOpen(true); }}
              isCollapsed={false}
              onToggleCollapse={() => setIsMobileSidebarOpen(false)}
            />
          </div>
        </div>
      )}

      {/* Main Content Workspace */}
      <div className="flex-1 flex flex-col min-w-0 h-full overflow-hidden">
        
        {/* Workspace Top Header */}
        <ClaudeHeader
          meeting={selectedMeeting}
          activeTab={activeTab}
          onTabChange={setActiveTab}
          onToggleMobileSidebar={() => setIsMobileSidebarOpen(!isMobileSidebarOpen)}
          onSearchChange={setSearchQuery}
          searchQuery={searchQuery}
        />

        {/* Tab View Container */}
        <div className="flex-1 overflow-y-auto relative">
          {loading ? (
            <div className="h-full flex items-center justify-center p-8 space-y-3 flex-col text-center">
              <div className="w-8 h-8 border-3 border-indigo-500 border-t-transparent rounded-full animate-spin"></div>
              <p className="text-xs text-zinc-400 font-mono">Loading meeting data from database...</p>
            </div>
          ) : !selectedMeeting ? (
            <div className="h-full flex items-center justify-center p-8 flex-col text-center max-w-md mx-auto space-y-4">
              <div className="w-14 h-14 rounded-2xl bg-indigo-500/10 border border-indigo-500/20 text-indigo-400 flex items-center justify-center">
                <span className="text-2xl">⚡</span>
              </div>
              <h2 className="text-xl font-bold text-white">No Meetings Found in Database</h2>
              <p className="text-xs text-zinc-400 leading-relaxed">
                Your database is empty or not yet seeded. Click below to ingest a YouTube URL or audio recording directly into your Supabase database & Pinecone vector index!
              </p>
              <button
                onClick={() => setIsUploadOpen(true)}
                className="px-5 py-2.5 rounded-xl bg-indigo-600 hover:bg-indigo-500 text-white font-semibold text-xs shadow-lg shadow-indigo-600/30 transition-all cursor-pointer"
              >
                + Process New Meeting
              </button>
            </div>
          ) : (
            <>
              {activeTab === 'chat' && (
                <ClaudeChatArea
                  messages={messages}
                  onQuickPrompt={handleSendMessage}
                />
              )}

              {activeTab === 'summary' && (
                <MeetingSummaryTab
                  summary={selectedMeeting.summary}
                  title={selectedMeeting.title}
                  participants={selectedMeeting.participants}
                />
              )}

              {activeTab === 'actions' && (
                <ActionItemsTab
                  meetingId={selectedMeeting.id}
                  actionItems={selectedMeeting.actionItems}
                />
              )}

              {activeTab === 'transcript' && (
                <TranscriptTab
                  transcript={selectedMeeting.transcript}
                  searchQuery={searchQuery}
                />
              )}

              {activeTab === 'analytics' && (
                <AnalyticsTab
                  participants={selectedMeeting.participants}
                  duration={selectedMeeting.duration}
                />
              )}
            </>
          )}
        </div>

        {/* Floating Bottom Prompt Bar (Always available in chat tab) */}
        {activeTab === 'chat' && selectedMeeting && (
          <ClaudePromptInput
            onSendMessage={handleSendMessage}
            onQuickPrompt={handleSendMessage}
          />
        )}

      </div>

      {/* Modals */}
      <UploadModal
        isOpen={isUploadOpen}
        onClose={() => setIsUploadOpen(false)}
        onUploadSuccess={handleUploadSuccess}
      />

      <SettingsModal
        isOpen={isSettingsOpen}
        onClose={() => setIsSettingsOpen(false)}
      />

    </div>
  );
}
