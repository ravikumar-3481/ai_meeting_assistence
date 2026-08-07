import os
import datetime
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
_audio_processor = AudioProcessor()
_transcriber = Transcriber()
_dir_manager = DirectoryManager()



_session_state = {"chunks": [], "embedding_vector": []}


def set_session_transcript(chunks: list, embedding_vector: list) -> None:
    """Call once after processing or loading a transcript so tools can use it."""
    _session_state["chunks"] = chunks
    _session_state["embedding_vector"] = embedding_vector


@tool
def search_meeting_transcript(question: str) -> str:
    """Search the currently loaded meeting transcript and answer a specific
    question about what was said, decided, or discussed."""
    if not _session_state["chunks"]:
        return "No transcript is loaded yet. Ask the user to process a meeting first."
    context = _embedding.get_context(
        question,
        _session_state["chunks"],
        _session_state["embedding_vector"],
    )
    if not context.strip():
        return "Nothing relevant found in the transcript for that question."
    return _models.generate_answers(context, question)


@tool
def get_top_discussion_topics() -> str:
    """Summarize the top 5 discussion topics and key information from the
    currently loaded meeting transcript."""
    if not _session_state["chunks"]:
        return "No transcript is loaded yet. Ask the user to process a meeting first."
    full_context = " ".join(_session_state["chunks"])
    return _models.generate_discussion_topics(full_context)


@tool
def process_new_meeting(source: str, language: str = "english") -> str:
    """Download or load an audio file, transcribe, chunk, and embed it so it
    becomes the active meeting transcript."""
    try:
        audio_chunks = _audio_processor.process_audio(source, language=language)
        transcript = _transcriber.transcribe(audio_chunks, language=language)
        text_chunks = _chunking.chunking(transcript)
        vectors = _embedding.embed_batch(text_chunks)

        # local session (existing behavior — unchanged)
        set_session_transcript(text_chunks, vectors)

        # NEW: persist to Pinecone under a unique meeting_id
        meeting_id = _tools.generate_meeting_id(source)
        _vector_store.store_embeddings(meeting_id, text_chunks, vectors)

        return (
            f"Meeting processed successfully as '{meeting_id}'. "
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