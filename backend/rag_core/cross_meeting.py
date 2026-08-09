from database.meeting import get_user_meetings
from models.models import AdvancedModels
from rag_core.vector_db import VectorStore
from utils.logger import Logger


class CrossMeetingSearch:
    def __init__(self):
        self.vector_store = VectorStore()
        self.advanced_models = AdvancedModels()
        self.log = Logger().get_logger()

    def _resolve_target_meetings(self, user_id: str, meeting_limit: int, since_date: str | None) -> list[dict]:
        meetings = get_user_meetings(user_id)
        if since_date:
            meetings = [m for m in meetings if str(m.get("created_at", "")) >= since_date]
        if meeting_limit:
            meetings = meetings[:meeting_limit]
        return meetings

    def _build_namespace_map(self, meetings: list[dict]) -> dict[str, dict]:
        namespace_map = {}
        for meeting in meetings:
            namespace = meeting.get("pinecone_namespace") or meeting.get("id")
            if namespace:
                namespace_map[namespace] = meeting
        return namespace_map

    def _fetch_matches_per_meeting(self, namespace_map: dict[str, dict], question: str, top_k_per_meeting: int) -> list[dict]:
        all_matches = []
        for namespace in namespace_map:
            matches = self.vector_store.query_cloud(question, top_k=top_k_per_meeting, meeting_ids=[namespace])
            all_matches.extend(matches)
        return all_matches

    def _build_context(self, matches: list[dict], namespace_map: dict[str, dict]) -> str:
        grouped: dict[tuple, list[str]] = {}

        for match in matches:
            namespace = match.get("meeting_id")
            meeting = namespace_map.get(namespace, {})
            title = meeting.get("title", namespace)
            created_at = str(meeting.get("created_at", match.get("date", "unknown date")))[:10]
            text = match.get("text", "")
            if not text.strip():
                continue
            key = (created_at, title, namespace)
            grouped.setdefault(key, []).append(text)

        ordered_keys = sorted(grouped.keys(), key=lambda k: k[0])
        blocks = []
        for created_at, title, _namespace in ordered_keys:
            texts = grouped[(created_at, title, _namespace)]
            lines = "\n".join(f"- {t}" for t in texts)
            blocks.append(f'[Meeting: "{title}" — {created_at}]\n{lines}')

        return "\n\n".join(blocks)

    def answer(
        self,
        user_id: str,
        question: str,
        meeting_limit: int = 5,
        top_k_per_meeting: int = 4,
        since_date: str | None = None,
    ) -> str:
        if not user_id or not user_id.strip():
            raise ValueError("user_id is required for cross-meeting search")
        if not question or not question.strip():
            raise ValueError("question is required for cross-meeting search")

        meetings = self._resolve_target_meetings(user_id, meeting_limit, since_date)
        if not meetings:
            return "No meetings found for this user yet."

        namespace_map = self._build_namespace_map(meetings)
        if not namespace_map:
            return "No meetings found for this user yet."

        matches = self._fetch_matches_per_meeting(namespace_map, question, top_k_per_meeting)
        if not matches:
            return "Nothing relevant found across these meetings for that question."

        context = self._build_context(matches, namespace_map)
        if not context.strip():
            return "Nothing relevant found across these meetings for that question."

        self.log.info(
            f"Cross-meeting search for user '{user_id}' spanned {len(namespace_map)} meetings, "
            f"{len(matches)} chunks retrieved."
        )
        return self.advanced_models.generate_cross_meeting_answer(context, question)