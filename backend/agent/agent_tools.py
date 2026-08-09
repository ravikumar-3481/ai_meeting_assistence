from langchain_core.tools import tool
from models.models import AdvancedModels
from agent.tools import get_session_transcript
from rag_core.vector_db import VectorStore
from utils.logger import Logger
from rag_core.cross_meeting import CrossMeetingSearch



_cross_meeting_search = CrossMeetingSearch()
log = Logger().get_logger()
_advanced_models = AdvancedModels()
_vector_store = VectorStore()


def _active_transcript() -> str:
    state = get_session_transcript()
    chunks = state.get("chunks", [])
    namespace = state.get("pinecone_namespace") or state.get("meeting_id")

    if chunks:
        return " ".join(chunks)
    elif namespace:
        matches = _vector_store.query_cloud("action items tasks meeting minutes decisions discussion overview", top_k=15, meeting_ids=[namespace])
        return " ".join([m["text"] for m in matches if m.get("text")])
    return ""


@tool
def extract_action_items() -> str:
    """Pull out every action item from the currently loaded meeting: what needs
    to be done, who owns it, and the deadline if one was mentioned. Use this
    when the user asks 'what do I need to do', 'what are the action items',
    or 'who owes what'."""
    transcript = _active_transcript()
    if not transcript:
        return "No transcript content available. Ask the user to process or select a meeting first."
    return _advanced_models.generate_action_items(transcript)


@tool
def generate_meeting_minutes() -> str:
    """Produce full formal meeting minutes (summary, topics, decisions, action
    items, open questions) from the currently loaded meeting. Use this when
    the user asks for 'minutes', 'formal notes', or a complete written record
    of the meeting rather than a quick recap."""
    transcript = _active_transcript()
    if not transcript:
        return "No transcript content available. Ask the user to process or select a meeting first."
    return _advanced_models.generate_meeting_minutes(transcript)


@tool
def draft_followup_email() -> str:
    """Draft a short, ready-to-send follow-up email recapping the currently
    loaded meeting for the attendees, including decisions and action items.
    Use this when the user asks to 'email the team', 'send a recap', or
    'draft a follow-up'."""
    transcript = _active_transcript()
    if not transcript:
        return "No transcript content available. Ask the user to process or select a meeting first."
    return _advanced_models.generate_followup_email(transcript)


@tool
def find_open_questions() -> str:
    """List questions and issues that came up in the currently loaded meeting
    but were never resolved or answered. Use this when the user asks 'what's
    still unresolved', 'what did we not decide', or 'what needs a follow-up'."""
    transcript = _active_transcript()
    if not transcript:
        return "No transcript content available. Ask the user to process or select a meeting first."
    return _advanced_models.generate_open_questions(transcript)


@tool
def find_disagreements() -> str:
    """Flag moments of real disagreement or unresolved tension in the
    currently loaded meeting, and note whether they got resolved. Use this
    when the user asks about pushback, conflict, or 'was there any
    disagreement'."""
    transcript = _active_transcript()
    if not transcript:
        return "No transcript content available. Ask the user to process or select a meeting first."
    return _advanced_models.generate_tension_points(transcript)


@tool
def search_across_meetings(question: str, meeting_limit: int = 5) -> str:
    """Answer a question that requires comparing or tracing a topic across
    multiple past meetings for the current user, such as how a decision or
    discussion changed over time. Use this instead of search_meeting_transcript
    when the user references more than one meeting, a time range, or asks
    about change, evolution, or history of a topic across meetings."""
    state = get_session_transcript()
    user_id = state.get("user_id")

    if not user_id:
        return "No active user session found. Ask the user to log in or load a meeting first."

    try:
        return _cross_meeting_search.answer(
            user_id=user_id,
            question=question,
            meeting_limit=meeting_limit,
        )
    except Exception as e:
        log.error(f"search_across_meetings failed: {e}")
        return f"Cross-meeting search failed: {e}"


ADVANCED_TOOLS = [
    extract_action_items,
    generate_meeting_minutes,
    draft_followup_email,
    find_open_questions,
    find_disagreements,
    search_across_meetings,
]