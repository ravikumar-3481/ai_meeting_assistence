# AI Meeting Assistant — Cloud-Only Multi-Chat Architecture

## Architecture Overview

The application implements a Claude / ChatGPT-style multi-chat system operating **purely over Cloud services** (Supabase Database + Pinecone Vector Store) without any local file persistence or local file reading:

1. **Supabase Database (`meetings` table)**:
   - Stores user meeting metadata: `id` (meeting_id), `user_id`, `title`, `source_url`, `language`, `status`, `pinecone_namespace`, `total_chunks`, `created_at`.
   - On user login, queries `SELECT id, title, created_at, pinecone_namespace FROM meetings WHERE user_id = :user_id ORDER BY created_at DESC`.

2. **Pinecone Vector Database**:
   - Stores text chunks and vectors namespaced per meeting (`namespace = meeting_id`).
   - Text chunks are saved within Pinecone vector metadata (`match.metadata['text']`).

3. **Cloud-Only Querying**:
   - When an existing meeting is selected from the menu, **zero local files are created or read**.
   - All tool invocations (`search_meeting_transcript`, `get_top_discussion_topics`, `extract_action_items`, `generate_meeting_minutes`, etc.) directly query **Pinecone Cloud** under `pinecone_namespace`.
   - Model generates answers using cloud-retrieved context.

4. **New Meeting Processing**:
   - Selecting `[+ Start New Meeting / New Chat]` processes a new audio URL or transcript source, upserts vectors + metadata into Pinecone, inserts meeting records into Supabase DB, and opens the new chat session.

---

## How to Test

Run the testing file:
```bash
python testing.py
```
1. **Log In** or **Sign Up** using Supabase Auth CLI.
2. Select any existing meeting chat from the Supabase DB list.
3. Ask questions (e.g. `what is agenda of this meeting`, `what are the action items`).
4. Type `exit` or `back` to return to the chat list and select another meeting or start a new chat!
