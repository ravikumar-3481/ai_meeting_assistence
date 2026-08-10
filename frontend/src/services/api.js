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
  // Authentication
  register: async (email, password, fullName) => {
    return request('/api/v1/auth/register', {
      method: 'POST',
      body: JSON.stringify({ email, password, full_name: fullName }),
    });
  },

  login: async (email, password) => {
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
    localStorage.removeItem('meeting_sense_token');
    localStorage.removeItem('meeting_sense_user');
  },

  getProfile: async () => {
    return request('/api/v1/auth/me', { method: 'GET' });
  },

  // Meetings
  getMeetings: async () => {
    return request('/api/v1/meetings', { method: 'GET' });
  },

  processMeeting: async (urlOrPath, language = 'english') => {
    return request('/api/v1/meetings/process', {
      method: 'POST',
      body: JSON.stringify({ url_or_path: urlOrPath, language }),
    });
  },

  loadMeeting: async (meetingId) => {
    return request('/api/v1/meetings/load', {
      method: 'POST',
      body: JSON.stringify({ meeting_id: meetingId }),
    });
  },

  getMeetingChunks: async (meetingId) => {
    return request(`/api/v1/meetings/${encodeURIComponent(meetingId)}/chunks`, { method: 'GET' });
  },

  getMeetingOutputs: async (meetingId) => {
    return request(`/api/v1/meetings/${encodeURIComponent(meetingId)}/outputs`, { method: 'GET' });
  },

  // Action Items
  getActionItems: async (meetingId) => {
    return request(`/api/v1/meetings/${encodeURIComponent(meetingId)}/action-items`, { method: 'GET' });
  },

  createActionItem: async (meetingId, task, owner, dueDate) => {
    return request(`/api/v1/meetings/${encodeURIComponent(meetingId)}/action-items`, {
      method: 'POST',
      body: JSON.stringify({ task, owner, due_date: dueDate }),
    });
  },

  updateActionItemStatus: async (actionItemId, status) => {
    return request(`/api/v1/action-items/${encodeURIComponent(actionItemId)}`, {
      method: 'PATCH',
      body: JSON.stringify({ status }),
    });
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
  sendChatQuery: async (meetingId, question, chatHistory = []) => {
    return request('/api/v1/chat/query', {
      method: 'POST',
      body: JSON.stringify({
        meeting_id: meetingId,
        question,
        chat_history: chatHistory.map((m) => ({
          role: m.sender === 'user' ? 'human' : 'assistant',
          content: m.text,
        })),
      }),
    });
  },

  // Audit Logs
  getAuditLogs: async () => {
    return request('/api/v1/audit-logs', { method: 'GET' });
  },
};
