CREATE EXTENSION IF NOT EXISTS pgcrypto;

-- ============ USERS ============
CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,
    full_name VARCHAR(255),
    created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

-- ============ MEETINGS ============
CREATE TABLE meetings (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    title VARCHAR(255) NOT NULL,
    source_url TEXT,
    language VARCHAR(20) DEFAULT 'english',
    status VARCHAR(20) DEFAULT 'processing',   -- processing | ready | failed
    pinecone_namespace VARCHAR(150) UNIQUE NOT NULL, -- "{user_id}_{meeting_id}"
    total_chunks INT DEFAULT 0,
    duration_seconds INT,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT now()
);
CREATE INDEX idx_meetings_user_id ON meetings(user_id);

-- ============ MEETING_CHUNKS (mapping only, no chunk text) ============
CREATE TABLE meeting_chunks (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    meeting_id UUID NOT NULL REFERENCES meetings(id) ON DELETE CASCADE,
    chunk_index INT NOT NULL,
    vector_id VARCHAR(100) NOT NULL,   -- Pinecone vector id
    created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    UNIQUE (meeting_id, chunk_index)
);
CREATE INDEX idx_chunks_meeting_id ON meeting_chunks(meeting_id);

-- ============ MEETING_OUTPUTS_META (log entry only, no content/path) ============
CREATE TABLE meeting_outputs_meta (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    meeting_id UUID NOT NULL REFERENCES meetings(id) ON DELETE CASCADE,
    output_type VARCHAR(30) NOT NULL,  -- topics | minutes | followup_email | open_questions | disagreements
    generated_at TIMESTAMPTZ NOT NULL DEFAULT now()
);
CREATE INDEX idx_outputs_meeting_id ON meeting_outputs_meta(meeting_id);

-- ============ ACTION ITEMS (small structured rows) ============
CREATE TABLE action_items (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    meeting_id UUID NOT NULL REFERENCES meetings(id) ON DELETE CASCADE,
    task TEXT NOT NULL,
    owner VARCHAR(255),
    due_date DATE,
    status VARCHAR(20) DEFAULT 'open',
    created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);
CREATE INDEX idx_action_items_meeting_id ON action_items(meeting_id);

-- ============ SESSIONS (auth tokens) ============
CREATE TABLE sessions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    token_hash TEXT NOT NULL,
    expires_at TIMESTAMPTZ NOT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);
CREATE INDEX idx_sessions_user_id ON sessions(user_id);

-- ============ AUDIT LOG (recommended) ============
CREATE TABLE access_audit_log (
    id BIGSERIAL PRIMARY KEY,
    user_id UUID REFERENCES users(id),
    meeting_id UUID REFERENCES meetings(id),
    action VARCHAR(50),
    accessed_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    result VARCHAR(20) -- allowed | denied
);