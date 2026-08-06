from langchain_core.tools import tool
from models.models import AdvancedModels
from agent.tools import _session_state  
from utils.logger import Logger

log = Logger().get_logger()
_advanced_models = AdvancedModels()



def _active_transcript() -> str:
    return " ".join(_session_state["chunks"])


@tool
def extract_action_items() -> str:
    """Pull out every action item from the currently loaded meeting: what needs
    to be done, who owns it, and the deadline if one was mentioned. Use this
    when the user asks 'what do I need to do', 'what are the action items',
    or 'who owes what'."""
    if not _session_state["chunks"]:
        return "No transcript is loaded yet. Ask the user to process a meeting first."
    return _advanced_models.generate_action_items(_active_transcript())


@tool
def generate_meeting_minutes() -> str:
    """Produce full formal meeting minutes (summary, topics, decisions, action
    items, open questions) from the currently loaded meeting. Use this when
    the user asks for 'minutes', 'formal notes', or a complete written record
    of the meeting rather than a quick recap."""
    if not _session_state["chunks"]:
        return "No transcript is loaded yet. Ask the user to process a meeting first."
    return _advanced_models.generate_meeting_minutes(_active_transcript())


@tool
def draft_followup_email() -> str:
    """Draft a short, ready-to-send follow-up email recapping the currently
    loaded meeting for the attendees, including decisions and action items.
    Use this when the user asks to 'email the team', 'send a recap', or
    'draft a follow-up'."""
    if not _session_state["chunks"]:
        return "No transcript is loaded yet. Ask the user to process a meeting first."
    return _advanced_models.generate_followup_email(_active_transcript())


@tool
def find_open_questions() -> str:
    """List questions and issues that came up in the currently loaded meeting
    but were never resolved or answered. Use this when the user asks 'what's
    still unresolved', 'what did we not decide', or 'what needs a follow-up'."""
    if not _session_state["chunks"]:
        return "No transcript is loaded yet. Ask the user to process a meeting first."
    return _advanced_models.generate_open_questions(_active_transcript())


@tool
def find_disagreements() -> str:
    """Flag moments of real disagreement or unresolved tension in the
    currently loaded meeting, and note whether they got resolved. Use this
    when the user asks about pushback, conflict, or 'was there any
    disagreement'."""
    if not _session_state["chunks"]:
        return "No transcript is loaded yet. Ask the user to process a meeting first."
    return _advanced_models.generate_tension_points(_active_transcript())


ADVANCED_TOOLS = [
    extract_action_items,
    generate_meeting_minutes,
    draft_followup_email,
    find_open_questions,
    find_disagreements,
]