import { clientCache, CACHE_TTL } from './cache';

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

function getAuthHeaders() {
  const token = localStorage.getItem('meeting_sense_token');
  return {
    'Content-Type': 'application/json',
    ...(token ? { Authorization: `Bearer ${token}` } : {}),
  };
}

async function request(endpoint, options = {}) {
  const url = `${API_BASE_URL}${endpoint}`;
  const headers = options.isFormData
    ? {
        ...(localStorage.getItem('meeting_sense_token')
          ? { Authorization: `Bearer ${localStorage.getItem('meeting_sense_token')}` }
          : {}),
      }
    : getAuthHeaders();

  const config = {
    ...options,
    headers: {
      ...headers,
      ...options.headers,
    },
  };

  try {
    const response = await fetch(url, config);
    const data = await response.json();
    if (!response.ok) {
      throw new Error(data.message || `Request failed with status ${response.status}`);
    }
    return data;
  } catch (err) {
    console.error(`API Error on ${endpoint}:`, err);
    throw err;
  }
}

export const api = {
  // Direct access to client cache
  cache: clientCache,

  // Authentication
  register: async (email, password, fullName) => {
    return request('/api/v1/auth/register', {
      method: 'POST',
      body: JSON.stringify({ email, password, full_name: fullName }),
    });
  },

  login: async (email, password) => {
    clientCache.clear();
    return request('/api/v1/auth/login', {
      method: 'POST',
      body: JSON.stringify({ email, password }),
    });
  },

  resetPassword: async (email) => {
    return request('/api/v1/auth/reset-password', {
      method: 'POST',
      body: JSON.stringify({ email }),
    });
  },

  logout: async () => {
    try {
      await request('/api/v1/auth/logout', { method: 'POST' });
    } catch (e) {
      console.warn('Logout API warning:', e);
    }
    clientCache.clear();
    localStorage.removeItem('meeting_sense_token');
    localStorage.removeItem('meeting_sense_user');
  },

  getProfile: async (options = {}) => {
    return clientCache.fetchWithCache(
      'profile:me',
      () => request('/api/v1/auth/me', { method: 'GET' }),
      { ttl: CACHE_TTL.PROFILE, forceRefresh: options.forceRefresh }
    );
  },

  // Meetings
  getMeetings: async (options = {}) => {
    return clientCache.fetchWithCache(
      'meetings:list',
      () => request('/api/v1/meetings', { method: 'GET' }),
      {
        ttl: CACHE_TTL.MEETINGS,
        forceRefresh: options.forceRefresh,
        staleWhileRevalidate: true,
      }
    );
  },

  processMeeting: async (urlOrPath, language = 'english') => {
    const res = await request('/api/v1/meetings/process', {
      method: 'POST',
      body: JSON.stringify({ url_or_path: urlOrPath, language }),
    });
    // Invalidate meetings list in cache
    clientCache.invalidate('meetings:list');
    return res;
  },

  loadMeeting: async (meetingId) => {
    const res = await request('/api/v1/meetings/load', {
      method: 'POST',
      body: JSON.stringify({ meeting_id: meetingId }),
    });
    clientCache.invalidate('meetings:list');
    return res;
  },

  getMeetingChunks: async (meetingId, options = {}) => {
    return clientCache.fetchWithCache(
      `chunks:${meetingId}`,
      () => request(`/api/v1/meetings/${encodeURIComponent(meetingId)}/chunks`, { method: 'GET' }),
      { ttl: CACHE_TTL.CHUNKS, persist: true, forceRefresh: options.forceRefresh }
    );
  },

  getMeetingOutputs: async (meetingId, options = {}) => {
    return clientCache.fetchWithCache(
      `outputs:${meetingId}`,
      () => request(`/api/v1/meetings/${encodeURIComponent(meetingId)}/outputs`, { method: 'GET' }),
      { ttl: CACHE_TTL.OUTPUTS, forceRefresh: options.forceRefresh }
    );
  },

  // Action Items
  getActionItems: async (meetingId, options = {}) => {
    return clientCache.fetchWithCache(
      `action_items:${meetingId}`,
      () => request(`/api/v1/meetings/${encodeURIComponent(meetingId)}/action-items`, { method: 'GET' }),
      { ttl: CACHE_TTL.ACTION_ITEMS, forceRefresh: options.forceRefresh }
    );
  },

  createActionItem: async (meetingId, task, owner, dueDate) => {
    const res = await request(`/api/v1/meetings/${encodeURIComponent(meetingId)}/action-items`, {
      method: 'POST',
      body: JSON.stringify({ task, owner, due_date: dueDate }),
    });
    // Invalidate cached action items for this meeting
    clientCache.invalidate(`action_items:${meetingId}`);
    return res;
  },

  updateActionItemStatus: async (actionItemId, status, meetingId = null) => {
    const res = await request(`/api/v1/action-items/${encodeURIComponent(actionItemId)}`, {
      method: 'PATCH',
      body: JSON.stringify({ status }),
    });
    // Invalidate cached action items
    if (meetingId) {
      clientCache.invalidate(`action_items:${meetingId}`);
    } else {
      clientCache.invalidate(/^action_items:/);
    }
    return res;
  },

  // Audio & Transcribe
  transcribeAudio: async (formData) => {
    return request('/api/v1/audio/transcribe', {
      method: 'POST',
      body: formData,
      isFormData: true,
    });
  },

  // AI Chat Agent Query
  sendChatQuery: async (meetingId, question, chatHistory = [], options = {}) => {
    const cacheKey = `chat:${meetingId}:${question.trim().toLowerCase()}:${chatHistory.length}`;
    return clientCache.fetchWithCache(
      cacheKey,
      () =>
        request('/api/v1/chat/query', {
          method: 'POST',
          body: JSON.stringify({
            meeting_id: meetingId,
            question,
            chat_history: chatHistory.map((m) => ({
              role: m.sender === 'user' ? 'human' : 'assistant',
              content: m.text,
            })),
          }),
        }),
      { ttl: CACHE_TTL.CHAT, forceRefresh: options.forceRefresh }
    );
  },

  // Audit Logs
  getAuditLogs: async () => {
    return request('/api/v1/audit-logs', { method: 'GET' });
  },
};

