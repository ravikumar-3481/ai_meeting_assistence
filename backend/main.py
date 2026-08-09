import sys
import argparse
import re
from typing import List, Tuple, Dict, Any, Optional
from langchain_core.messages import HumanMessage, AIMessage
from rag_core.cross_meeting import CrossMeetingSearch
from utils.logger import Logger
from agent.agent_core import MeetingAgent
from rag_core.rag_pipline import RagPipeline
from database.meeting import get_user_meetings

# Database Operations Imports (schema.sql tables)
from database.operations import (
    get_user_profile,
    update_user_profile,
    get_chunks_by_meeting,
    insert_output_meta,
    get_outputs_meta_by_meeting,
    insert_action_item,
    bulk_insert_action_items,
    get_action_items_by_meeting,
    update_action_item_status,
    insert_audit_log,
    get_audit_logs_by_user,
    get_audit_logs_by_meeting,
)

# Initialize Logger
log = Logger().get_logger()

# Global Constants
MAX_HISTORY_TURNS = 6  # Maintains last N turns (12 messages total) to preserve context window
DEFAULT_USER_ID = "default_user"
DEFAULT_LANGUAGE = "english"


# =============================================================================
# BACKEND CORE SERVICES (Reusable by FastAPI / Streamlit / Flask in future)
# =============================================================================

def process_new_meeting(
    url_or_path: str,
    user_id: str = DEFAULT_USER_ID,
    language: str = DEFAULT_LANGUAGE
) -> Tuple[str, str]:
    log.info(f"Initiating RAG pipeline for source: '{url_or_path}' (User: '{user_id}')")
    pipeline = RagPipeline()
    meeting_id, title = pipeline.rag_pipeline(url=url_or_path, user_id=user_id, language=language)

    # Record output metadata & access audit log in database
    try:
        insert_output_meta(meeting_id=meeting_id, output_type="ingestion_pipeline")
        insert_audit_log(user_id=user_id, meeting_id=meeting_id, action="process_new_meeting", result="allowed")
    except Exception as e:
        log.warning(f"Audit/Meta tracking notice during ingestion: {e}")

    return meeting_id, title


def load_existing_meeting(
    meeting_id: str,
    user_id: str = DEFAULT_USER_ID
) -> Tuple[str, str]:
    log.info(f"Loading existing meeting '{meeting_id}' for user '{user_id}'...")
    pipeline = RagPipeline()
    meeting_id, title = pipeline.load_existing_meeting_session(user_id=user_id, meeting_id=meeting_id)

    # Record access audit log in database
    try:
        insert_audit_log(user_id=user_id, meeting_id=meeting_id, action="load_existing_meeting", result="allowed")
    except Exception as e:
        log.warning(f"Audit log notice: {e}")

    return meeting_id, title


def fetch_user_meeting_list(user_id: str = DEFAULT_USER_ID) -> List[Dict[str, Any]]:
    try:
        return get_user_meetings(user_id=user_id)
    except Exception as e:
        log.error(f"Failed to fetch meetings for user '{user_id}': {e}")
        return []


def query_meeting_agent(
    agent: MeetingAgent,
    question: str,
    chat_history: List[Any],
    session_id: Optional[str] = None
) -> Tuple[str, List[Any]]:
    if not question or not question.strip():
        return "Please ask a valid question.", chat_history

    # Audit log entry for agent query
    if session_id and ":" in session_id:
        parts = session_id.split(":", 1)
        u_id, m_id = parts[0], parts[1]
        try:
            insert_audit_log(user_id=u_id, meeting_id=m_id, action="query_agent", result="allowed")
        except Exception:
            pass

    # Execute Agent query
    raw_answer = agent.run(user_input=question, chat_history=chat_history, session_id=session_id)
    clean_answer = re.sub(r"^\s+|\s+$", "", raw_answer).strip()

    # Append question and answer to chat history
    updated_history = list(chat_history)
    updated_history.append(HumanMessage(content=question))
    updated_history.append(AIMessage(content=clean_answer))

    # Trim history to maintain MAX_HISTORY_TURNS (each turn has 2 messages: Human + AI)
    trimmed_history = updated_history[-(MAX_HISTORY_TURNS * 2):]

    return clean_answer, trimmed_history


# =============================================================================
# ADDITIONAL DATABASE OPERATIONS SERVICE HELPERS
# =============================================================================

def fetch_user_profile(user_id: str) -> Optional[Dict[str, Any]]:
    """Retrieves user profile data from public.users table."""
    try:
        return get_user_profile(user_id=user_id)
    except Exception as e:
        log.error(f"Failed to fetch user profile for '{user_id}': {e}")
        return None


def fetch_meeting_action_items(meeting_id: str, status: Optional[str] = None) -> List[Dict[str, Any]]:
    """Retrieves action items associated with a meeting from public.action_items table."""
    try:
        return get_action_items_by_meeting(meeting_id=meeting_id, status=status)
    except Exception as e:
        log.error(f"Failed to fetch action items for meeting '{meeting_id}': {e}")
        return []


def create_meeting_action_item(
    meeting_id: str,
    task: str,
    owner: Optional[str] = None,
    due_date: Optional[str] = None
) -> Dict[str, Any]:
    """Creates a new action item in public.action_items table."""
    try:
        return insert_action_item(meeting_id=meeting_id, task=task, owner=owner, due_date=due_date)
    except Exception as e:
        log.error(f"Failed to insert action item for meeting '{meeting_id}': {e}")
        return {}


def fetch_meeting_chunks_meta(meeting_id: str) -> List[Dict[str, Any]]:
    """Retrieves meeting chunks vector references from public.meeting_chunks table."""
    try:
        return get_chunks_by_meeting(meeting_id=meeting_id)
    except Exception as e:
        log.error(f"Failed to fetch meeting chunks for '{meeting_id}': {e}")
        return []


def fetch_meeting_outputs_history(meeting_id: str) -> List[Dict[str, Any]]:
    """Retrieves metadata history for outputs generated for a meeting."""
    try:
        return get_outputs_meta_by_meeting(meeting_id=meeting_id)
    except Exception as e:
        log.error(f"Failed to fetch output metadata for '{meeting_id}': {e}")
        return []


def fetch_user_audit_logs(user_id: str, limit: int = 50) -> List[Dict[str, Any]]:
    """Retrieves access audit log records for a user."""
    try:
        return get_audit_logs_by_user(user_id=user_id, limit=limit)
    except Exception as e:
        log.error(f"Failed to fetch audit logs for user '{user_id}': {e}")
        return []



def query_cross_meeting_trend(
    question: str,
    user_id: str = DEFAULT_USER_ID,
    meeting_limit: int = 5
) -> str:
    searcher = CrossMeetingSearch()
    return searcher.answer(user_id=user_id, question=question, meeting_limit=meeting_limit)
# =============================================================================
# INTERACTIVE CLI INTERFACE (For Local Testing & Developer Usage)
# =============================================================================

def run_chat_session(
    agent: MeetingAgent,
    meeting_id: str,
    title: str,
    user_id: str = DEFAULT_USER_ID
) -> None:
    session_id = f"{user_id}:{meeting_id}"
    chat_history: List[Any] = []

    print("\n" + "=" * 70)
    print(f" ACTIVE MEETING SESSION: {title}")
    print(f" Meeting ID : {meeting_id}")
    print(f" Session ID : {session_id}")
    print("=" * 70)
    log.info("[bold green]Agent ready.[/bold green] Ask anything about this meeting (type 'exit' or 'back' to return).\n")

    while True:
        try:
            user_input = input("\nYou: ").strip()
        except (KeyboardInterrupt, EOFError):
            print("\nExiting session...")
            break

        if not user_input:
            continue

        if user_input.lower() in ("exit", "quit", "back"):
            log.info("Ending chat session.")
            break

        answer, chat_history = query_meeting_agent(
            agent=agent,
            question=user_input,
            chat_history=chat_history,
            session_id=session_id
        )

        print(f"\nAgent: {answer}")


def interactive_cli_menu(user_id: str = DEFAULT_USER_ID, language: str = DEFAULT_LANGUAGE) -> None:
    agent = MeetingAgent(verbose=False)

    while True:
        print("\n" + "=" * 60)
        print(" AI MEETING ASSISTANT - MAIN MENU")
        print("=" * 60)
        print(" 1. Process New Meeting (YouTube URL or Local .txt Transcript)")
        print(" 2. Load Existing Meeting from Supabase DB")
        print(" 3. List My Past Meetings")
        print(" 4. View Action Items for a Meeting")
        print(" 5. View User Audit Logs")
        print(" 0. Exit")
        print("=" * 60)

        try:
            choice = input("\nSelect an option (0-5): ").strip()
        except (KeyboardInterrupt, EOFError):
            print("\nExiting application. Goodbye!")
            sys.exit(0)

        if choice == "1":
            url_or_path = input("\nEnter YouTube URL or local transcript path (.txt): ").strip()
            if not url_or_path:
                log.warning("No input provided.")
                continue

            try:
                meeting_id, title = process_new_meeting(
                    url_or_path=url_or_path,
                    user_id=user_id,
                    language=language
                )
                run_chat_session(agent=agent, meeting_id=meeting_id, title=title, user_id=user_id)
            except Exception as e:
                log.error(f"Failed to process meeting: {e}")

        elif choice == "2":
            meeting_id = input("\nEnter Existing Meeting ID or Pinecone Namespace: ").strip()
            if not meeting_id:
                log.warning("Meeting ID cannot be empty.")
                continue

            try:
                meeting_id, title = load_existing_meeting(meeting_id=meeting_id, user_id=user_id)
                run_chat_session(agent=agent, meeting_id=meeting_id, title=title, user_id=user_id)
            except Exception as e:
                log.error(f"Failed to load meeting: {e}")

        elif choice == "3":
            print(f"\nFetching meetings for user '{user_id}'...")
            meetings = fetch_user_meeting_list(user_id=user_id)
            if not meetings:
                print("No meetings found for this user.")
            else:
                print(f"\nFound {len(meetings)} meeting(s):")
                print("-" * 60)
                for idx, m in enumerate(meetings, 1):
                    m_id = m.get("id") or m.get("pinecone_namespace")
                    m_title = m.get("title", "Untitled")
                    m_status = m.get("status", "unknown")
                    m_chunks = m.get("total_chunks", 0)
                    print(f" {idx}. [{m_id}] {m_title} (Chunks: {m_chunks}, Status: {m_status})")
                print("-" * 60)

        elif choice == "4":
            m_id = input("\nEnter Meeting ID: ").strip()
            if not m_id:
                log.warning("Meeting ID required.")
                continue
            items = fetch_meeting_action_items(meeting_id=m_id)
            print(f"\nAction Items for '{m_id}': {len(items)}")
            for item in items:
                print(f" - [{item.get('status', 'open')}] Task: {item.get('task')} | Owner: {item.get('owner')} | Due: {item.get('due_date')}")

        elif choice == "5":
            logs = fetch_user_audit_logs(user_id=user_id)
            print(f"\nAudit Logs for User '{user_id}': {len(logs)}")
            for l in logs:
                print(f" - [{l.get('accessed_at')[:19]}] Action: {l.get('action')} | Result: {l.get('result')} | Meeting: {l.get('meeting_id')}")

        elif choice == "0":
            log.info("Exiting AI Meeting Assistance. Goodbye!")
            sys.exit(0)
        else:
            log.warning("Invalid choice. Please select an option between 0 and 5.")


# =============================================================================
# CLI PARSER & MAIN ENTRY POINT
# =============================================================================

def parse_cli_args() -> argparse.Namespace:
    """Parses command line arguments for non-interactive execution."""
    parser = argparse.ArgumentParser(
        description="AI Meeting Assistance - Process meetings and chat with AI Agent."
    )
    parser.add_argument("--url", type=str, help="YouTube URL or local text transcript file path (.txt)")
    parser.add_argument("--meeting-id", type=str, help="Existing meeting ID to load directly")
    parser.add_argument("--user-id", type=str, default=DEFAULT_USER_ID, help="User ID for session management")
    parser.add_argument("--language", type=str, default=DEFAULT_LANGUAGE, help="Language (e.g. 'english', 'hinglish')")
    return parser.parse_args()


def main() -> None:
    """Main application entry point."""
    args = parse_cli_args()

    # Direct execution mode if arguments are supplied via CLI
    if args.url:
        meeting_id, title = process_new_meeting(
            url_or_path=args.url,
            user_id=args.user_id,
            language=args.language
        )
        agent = MeetingAgent(verbose=False)
        run_chat_session(agent=agent, meeting_id=meeting_id, title=title, user_id=args.user_id)

    elif args.meeting_id:
        meeting_id, title = load_existing_meeting(
            meeting_id=args.meeting_id,
            user_id=args.user_id
        )
        agent = MeetingAgent(verbose=False)
        run_chat_session(agent=agent, meeting_id=meeting_id, title=title, user_id=args.user_id)

    else:
        # Interactive CLI menu if no direct arguments are provided
        interactive_cli_menu(user_id=args.user_id, language=args.language)


if __name__ == "__main__":
    main()