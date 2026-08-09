import os
import datetime
import contextvars
from langchain_core.tools import tool
from rag_core.embedding import Embeddings
from rag_core.chunking import Chunking
from models.models import Models
from audio.audio_processor import AudioProcessor
from audio.transcribe import Transcriber
from utils.tools import DirectoryManager
from utils.logger import Logger
from rag_core.vector_db import VectorStore
from utils.tools import Tools

log = Logger().get_logger()
_vector_store = VectorStore()
_tools = Tools()

_embedding = Embeddings()
_chunking = Chunking()
_models = Models()
_transcriber = Transcriber()
_dir_manager = DirectoryManager()

_audio_processor_instance = None


def get_audio_processor() -> AudioProcessor:
    global _audio_processor_instance
    if _audio_processor_instance is None:
        _audio_processor_instance = AudioProcessor()
    return _audio_processor_instance


_active_session_id: contextvars.ContextVar[str] = contextvars.ContextVar("active_session_id", default="default")
_sessions_store: dict[str, dict] = {}


def set_active_session_id(session_id: str) -> None:
    _active_session_id.set(session_id)


def get_active_session_id() -> str:
    return _active_session_id.get()


def set_session_transcript(
    chunks: list | None = None,
    embedding_vector: list | None = None,
    session_id: str | None = None,
    meeting_id: str | None = None,
    pinecone_namespace: str | None = None,
    user_id: str | None = None,
) -> None:
    sid = session_id or get_active_session_id()
    existing = _sessions_store.get(sid, {})
    _sessions_store[sid] = {
        "chunks": chunks if chunks is not None else existing.get("chunks", []),
        "embedding_vector": embedding_vector if embedding_vector is not None else existing.get("embedding_vector", []),
        "meeting_id": meeting_id or existing.get("meeting_id", ""),
        "pinecone_namespace": pinecone_namespace or existing.get("pinecone_namespace", meeting_id or ""),
        "user_id": user_id or existing.get("user_id", ""),
    }


def get_session_transcript(session_id: str | None = None) -> dict:
    sid = session_id or get_active_session_id()
    default_state = {"chunks": [], "embedding_vector": [], "meeting_id": "", "pinecone_namespace": "", "user_id": ""}
    state = _sessions_store.get(sid, default_state)

    if not state.get("user_id") and ":" in sid:
        state = dict(state)
        state["user_id"] = sid.split(":", 1)[0]

    return state


def clear_session_transcript(session_id: str | None = None) -> None:
    sid = session_id or get_active_session_id()
    _sessions_store.pop(sid, None)


class _SessionStateProxy(dict):
    """Backwards-compatibility proxy for _session_state imports."""
    def __getitem__(self, key):
        return get_session_transcript().get(key, [])

    def __setitem__(self, key, value):
        state = get_session_transcript()
        state[key] = value
        set_session_transcript(
            chunks=state.get("chunks", []),
            embedding_vector=state.get("embedding_vector", []),
            meeting_id=state.get("meeting_id", ""),
            pinecone_namespace=state.get("pinecone_namespace", ""),
        )

    def get(self, key, default=None):
        return get_session_transcript().get(key, default)


_session_state = _SessionStateProxy({"chunks": [], "embedding_vector": []})


@tool
def search_meeting_transcript(question: str) -> str:
    """Search the currently loaded meeting transcript and answer a specific
    question about what was said, decided, or discussed."""
    state = get_session_transcript()
    chunks = state.get("chunks", [])
    embedding_vector = state.get("embedding_vector", [])
    namespace = state.get("pinecone_namespace") or state.get("meeting_id")

    if chunks and embedding_vector:
        context = _embedding.get_context(question, chunks, embedding_vector)
    elif namespace:
        matches = _vector_store.query_cloud(question, top_k=5, meeting_ids=[namespace])
        context = " ".join([m["text"] for m in matches if m.get("text")])
    else:
        return "No transcript is loaded yet. Ask the user to process or select a meeting first."

    if not context.strip():
        return "Nothing relevant found in the transcript for that question."
    return _models.generate_answers(context, question)


@tool
def get_top_discussion_topics() -> str:
    """Summarize the top 5 discussion topics and key information from the
    currently loaded meeting transcript."""
    state = get_session_transcript()
    chunks = state.get("chunks", [])
    namespace = state.get("pinecone_namespace") or state.get("meeting_id")

    if chunks:
        full_context = " ".join(chunks)
    elif namespace:
        matches = _vector_store.query_cloud("discussion topics main agenda key points summary", top_k=10, meeting_ids=[namespace])
        full_context = " ".join([m["text"] for m in matches if m.get("text")])
    else:
        return "No transcript is loaded yet. Ask the user to process or select a meeting first."

    if not full_context.strip():
        return "No transcript content found for this meeting."
    return _models.generate_discussion_topics(full_context)


@tool
def process_new_meeting(source: str, language: str = "english") -> str:
    """Download or load an audio file, transcribe, chunk, and embed it so it
    becomes the active meeting transcript."""
    try:
        audio_processor = get_audio_processor()
        audio_chunks = audio_processor.process_audio(source, language=language)
        transcript = _transcriber.transcribe(audio_chunks, language=language)
        text_chunks = _chunking.chunking(transcript)
        vectors = _embedding.embed_batch(text_chunks)

        meeting_id, title = _tools.generate_meeting_id(source)
        set_session_transcript(text_chunks, vectors, meeting_id=meeting_id, pinecone_namespace=meeting_id)
        _vector_store.store_embeddings(meeting_id, text_chunks, vectors)

        return (
            f"Meeting processed successfully as '{meeting_id}' ('{title}'). "
            f"{len(text_chunks)} chunks are ready for search and summary."
        )
    except Exception as e:
        log.error(f"process_new_meeting failed: {e}")
        return f"Failed to process meeting: {e}"


@tool
def save_summary_to_file(content: str, filename: str = "meeting_summary.txt") -> str:
    """Save a summary, answer, or note to a text file."""
    path = _dir_manager.save_to_dir(content, "data/outputs", filename)
    return f"Saved to {path}"


@tool
def get_current_datetime() -> str:
    """Return today's date and time."""
    return datetime.datetime.now().strftime("%A, %B %d, %Y %I:%M %p")


ALL_TOOLS = [
    search_meeting_transcript,
    get_top_discussion_topics,
    process_new_meeting,
    save_summary_to_file,
    get_current_datetime,
]