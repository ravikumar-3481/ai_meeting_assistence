import os
import tempfile
import time
from typing import List, Dict, Any, Optional

from fastapi import (
    FastAPI,
    Depends,
    HTTPException,
    Security,
    status,
    Request,
    Response,
    UploadFile,
    File,
    Form,
    Query,
    Path,
)
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi.responses import JSONResponse
from langchain_core.messages import HumanMessage, AIMessage
import uvicorn

from utils.logger import Logger
from api.config import Config
from authentication.auth_model import AuthService
from database.client import get_user_client
from database.operations import (
    get_user_profile,
    update_user_profile,
    update_action_item_status,
)
from main import (
    process_new_meeting,
    load_existing_meeting,
    fetch_user_meeting_list,
    query_meeting_agent,
    fetch_meeting_chunks_meta,
    fetch_meeting_outputs_history,
    fetch_meeting_action_items,
    create_meeting_action_item,
    fetch_user_audit_logs,
    fetch_user_profile,
)
from agent.agent_core import MeetingAgent
from audio.transcribe import Transcriber
from audio.audio_processor import AudioProcessor
from rag_core.vector_db import VectorStore
from models.models import Models

from schemas import (
    APIResponse,
    UserCreate,
    UserLogin,
    MeetingProcessRequest,
    MeetingLoadRequest,
    ActionItemCreate,
    ActionItemUpdate,
    ChatQueryRequest,
)

log = Logger().get_logger()

app = FastAPI(
    title="AI Meeting Assistance Secure API",
    description="Backend API for processing, analyzing, searching, and chatting with meeting notes and transcriptions.",
    version="1.0.0",
)

security_bearer = HTTPBearer(auto_error=False)

AGENT_SESSION_CACHE: Dict[str, MeetingAgent] = {}
_vector_store = VectorStore()
_qa_model = Models()


ALLOWED_ORIGINS = [o.strip() for o in os.environ.get("ALLOWED_ORIGINS", "*").split(",")]

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials="*" not in ALLOWED_ORIGINS,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.middleware("http")
async def security_headers_and_logging_middleware(request: Request, call_next):
    start_time = time.time()
    response: Response = await call_next(request)
    process_time = time.time() - start_time

    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["X-XSS-Protection"] = "1; mode=block"
    response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
    response.headers["X-Process-Time"] = f"{process_time:.4f}s"

    log.info(f"{request.method} {request.url.path} -> {response.status_code} ({process_time:.4f}s)")
    return response


@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"success": False, "message": exc.detail, "data": None},
    )


@app.exception_handler(Exception)
async def generic_exception_handler(request: Request, exc: Exception):
    log.error(f"Unhandled exception on '{request.url.path}': {exc}", exc_info=True)
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"success": False, "message": "Internal server error.", "data": None},
    )


async def get_current_user(
    credentials: Optional[HTTPAuthorizationCredentials] = Security(security_bearer),
) -> Dict[str, Any]:
    if not credentials or not credentials.credentials:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication required.",
            headers={"WWW-Authenticate": "Bearer"},
        )

    token = credentials.credentials

    try:
        user_client = get_user_client(access_token=token)
        supabase_user_resp = user_client.auth.get_user(jwt=token)

        if not supabase_user_resp or not supabase_user_resp.user:
            raise ValueError("Invalid user token or expired session.")

        user = supabase_user_resp.user

        profile = None
        try:
            profile = get_user_profile(user.id)
        except Exception:
            pass

        full_name = profile.get("full_name") if profile else user.user_metadata.get("full_name")

        return {
            "id": user.id,
            "email": user.email,
            "full_name": full_name,
            "access_token": token,
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Invalid or expired token: {e}",
            headers={"WWW-Authenticate": "Bearer"},
        )


def get_agent_for_session(user_id: str, meeting_id: str) -> MeetingAgent:
    session_key = f"{user_id}:{meeting_id}"
    if session_key not in AGENT_SESSION_CACHE:
        AGENT_SESSION_CACHE[session_key] = MeetingAgent(verbose=False)
    return AGENT_SESSION_CACHE[session_key]


def query_cross_meeting_trend(question: str, user_id: str, meeting_limit: int = 5) -> str:
    meetings = fetch_user_meeting_list(user_id=user_id)[:meeting_limit]
    namespaces = [m.get("pinecone_namespace") or m.get("id") for m in meetings]
    namespaces = [ns for ns in namespaces if ns]

    if not namespaces:
        return "No meetings found for this user to search across."

    matches = _vector_store.query_cloud(question, top_k=10, meeting_ids=namespaces)
    context = " ".join(m["text"] for m in matches if m.get("text"))

    if not context.strip():
        return "Nothing relevant found across your meetings for that question."

    return _qa_model.generate_answers(context, question)


@app.get("/health", response_model=APIResponse, tags=["System"])
async def health_check():
    config = Config()
    return APIResponse(
        success=True,
        message="AI Meeting Assistance backend is running.",
        data={
            "status": "healthy",
            "environment": config.pinecone_cloud,
            "supabase_connected": bool(config.supabase_url),
        },
    )


@app.post("/api/v1/auth/register", response_model=APIResponse, tags=["Authentication"])
async def register(payload: UserCreate):
    auth_service = AuthService()
    try:
        result = auth_service.sign_up(
            email=payload.email,
            password=payload.password,
            full_name=payload.full_name,
        )
        return APIResponse(
            success=True,
            message="User registered successfully.",
            data={
                "user_id": result.user_id,
                "email": result.email,
                "access_token": result.access_token,
                "refresh_token": result.refresh_token,
            },
        )
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Registration failed: {e}")


@app.post("/api/v1/auth/login", response_model=APIResponse, tags=["Authentication"])
async def login(payload: UserLogin):
    auth_service = AuthService()
    try:
        result = auth_service.sign_in(email=payload.email, password=payload.password)
        return APIResponse(
            success=True,
            message="Login successful.",
            data={
                "user_id": result.user_id,
                "email": result.email,
                "access_token": result.access_token,
                "refresh_token": result.refresh_token,
            },
        )
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=f"Sign-in failed: {e}")


@app.post("/api/v1/auth/logout", response_model=APIResponse, tags=["Authentication"])
async def logout(current_user: Dict[str, Any] = Depends(get_current_user)):
    auth_service = AuthService()
    try:
        auth_service.sign_out(access_token=current_user["access_token"])
    except Exception as e:
        log.warning(f"Sign-out non-fatal error: {e}")
    return APIResponse(success=True, message="Logged out.", data=None)


@app.get("/api/v1/auth/me", response_model=APIResponse, tags=["User Profile"])
async def get_my_profile(current_user: Dict[str, Any] = Depends(get_current_user)):
    profile = fetch_user_profile(current_user["id"]) or current_user
    return APIResponse(success=True, message="Profile fetched.", data=profile)


@app.put("/api/v1/auth/profile", response_model=APIResponse, tags=["User Profile"])
async def update_my_profile(
    full_name: Optional[str] = Query(None),
    email: Optional[str] = Query(None),
    current_user: Dict[str, Any] = Depends(get_current_user),
):
    try:
        updated = update_user_profile(user_id=current_user["id"], full_name=full_name, email=email)
        return APIResponse(success=True, message="Profile updated.", data=updated)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Update failed: {e}")


@app.post("/api/v1/meetings/process", response_model=APIResponse, tags=["Meetings"])
async def api_process_meeting(
    payload: MeetingProcessRequest,
    current_user: Dict[str, Any] = Depends(get_current_user),
):
    user_id = current_user["id"]
    try:
        meeting_id, title = process_new_meeting(
            url_or_path=payload.url_or_path,
            user_id=user_id,
            language=payload.language.value,
        )
        return APIResponse(
            success=True,
            message="Meeting processed and indexed.",
            data={"meeting_id": meeting_id, "title": title, "user_id": user_id},
        )
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Processing failed: {e}")


@app.post("/api/v1/meetings/load", response_model=APIResponse, tags=["Meetings"])
async def api_load_meeting(
    payload: MeetingLoadRequest,
    current_user: Dict[str, Any] = Depends(get_current_user),
):
    user_id = current_user["id"]
    try:
        meeting_id, title = load_existing_meeting(meeting_id=payload.meeting_id, user_id=user_id)
        return APIResponse(
            success=True,
            message="Meeting loaded.",
            data={"meeting_id": meeting_id, "title": title, "user_id": user_id},
        )
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Load failed: {e}")


@app.get("/api/v1/meetings", response_model=APIResponse, tags=["Meetings"])
async def list_meetings(current_user: Dict[str, Any] = Depends(get_current_user)):
    meetings = fetch_user_meeting_list(user_id=current_user["id"])
    return APIResponse(success=True, message=f"Retrieved {len(meetings)} meetings.", data=meetings)


@app.get("/api/v1/meetings/{meeting_id}/chunks", response_model=APIResponse, tags=["Meetings"])
async def get_meeting_chunks(
    meeting_id: str = Path(...),
    current_user: Dict[str, Any] = Depends(get_current_user),
):
    chunks = fetch_meeting_chunks_meta(meeting_id)
    return APIResponse(success=True, message=f"Retrieved {len(chunks)} chunks.", data=chunks)


@app.get("/api/v1/meetings/{meeting_id}/outputs", response_model=APIResponse, tags=["Meetings"])
async def get_meeting_outputs(
    meeting_id: str = Path(...),
    current_user: Dict[str, Any] = Depends(get_current_user),
):
    outputs = fetch_meeting_outputs_history(meeting_id)
    return APIResponse(success=True, message=f"Retrieved {len(outputs)} output records.", data=outputs)


@app.post("/api/v1/audio/transcribe", response_model=APIResponse, tags=["Audio & Speech"])
async def api_transcribe_audio(
    file: Optional[UploadFile] = File(None),
    url: Optional[str] = Form(None),
    language: str = Form("english"),
    current_user: Dict[str, Any] = Depends(get_current_user),
):
    if not file and not url:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Provide an audio file or a URL.")

    transcriber = Transcriber()
    processor = AudioProcessor()
    temp_path = None

    try:
        if file:
            suffix = os.path.splitext(file.filename or ".wav")[1]
            with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
                content = await file.read()
                tmp.write(content)
                temp_path = tmp.name
            audio_source = temp_path
        else:
            audio_source = url

        chunks = processor.process_audio(url=audio_source, language=language)
        if not chunks:
            raise ValueError("No audio chunks could be generated.")

        transcript = transcriber.transcribe(chunks=chunks, language=language)

        return APIResponse(
            success=True,
            message="Audio transcribed.",
            data={"language": language, "chunks_processed": len(chunks), "transcript": transcript},
        )
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Transcription failed: {e}")
    finally:
        if temp_path and os.path.exists(temp_path):
            os.remove(temp_path)


@app.post("/api/v1/chat/query", response_model=APIResponse, tags=["AI Agent & Chat"])
async def api_chat_query(
    payload: ChatQueryRequest,
    current_user: Dict[str, Any] = Depends(get_current_user),
):
    user_id = current_user["id"]
    session_id = f"{user_id}:{payload.meeting_id}"

    try:
        agent = get_agent_for_session(user_id=user_id, meeting_id=payload.meeting_id)

        chat_history = []
        for msg in payload.chat_history:
            if msg.role.lower() in ("human", "user"):
                chat_history.append(HumanMessage(content=msg.content))
            elif msg.role.lower() in ("ai", "assistant"):
                chat_history.append(AIMessage(content=msg.content))

        answer, updated_history = query_meeting_agent(
            agent=agent,
            question=payload.question,
            chat_history=chat_history,
            session_id=session_id,
        )

        return APIResponse(
            success=True,
            message="Query executed.",
            data={
                "meeting_id": payload.meeting_id,
                "session_id": session_id,
                "answer": answer,
                "history_length": len(updated_history),
            },
        )
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Agent query failed: {e}")


@app.post("/api/v1/chat/cross-meeting", response_model=APIResponse, tags=["AI Agent & Chat"])
async def api_cross_meeting_query(
    question: str = Query(...),
    meeting_limit: int = Query(5, ge=1, le=20),
    current_user: Dict[str, Any] = Depends(get_current_user),
):
    try:
        answer = query_cross_meeting_trend(
            question=question, user_id=current_user["id"], meeting_limit=meeting_limit
        )
        return APIResponse(
            success=True,
            message="Cross-meeting search completed.",
            data={"question": question, "meeting_limit": meeting_limit, "answer": answer},
        )
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Cross-meeting search failed: {e}")


@app.get("/api/v1/meetings/{meeting_id}/action-items", response_model=APIResponse, tags=["Action Items"])
async def get_action_items(
    meeting_id: str = Path(...),
    status_filter: Optional[str] = Query(None, alias="status"),
    current_user: Dict[str, Any] = Depends(get_current_user),
):
    items = fetch_meeting_action_items(meeting_id=meeting_id, status=status_filter)
    return APIResponse(success=True, message=f"Fetched {len(items)} action items.", data=items)


@app.post("/api/v1/meetings/{meeting_id}/action-items", response_model=APIResponse, tags=["Action Items"])
async def create_action_item(
    payload: ActionItemCreate,
    meeting_id: str = Path(...),
    current_user: Dict[str, Any] = Depends(get_current_user),
):
    try:
        created = create_meeting_action_item(
            meeting_id=meeting_id,
            task=payload.task,
            owner=payload.owner,
            due_date=payload.due_date,
        )
        return APIResponse(success=True, message="Action item created.", data=created)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Creation failed: {e}")


@app.patch("/api/v1/action-items/{action_item_id}", response_model=APIResponse, tags=["Action Items"])
async def patch_action_item_status(
    payload: ActionItemUpdate,
    action_item_id: str = Path(...),
    current_user: Dict[str, Any] = Depends(get_current_user),
):
    if payload.status is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="status is required.")

    try:
        updated = update_action_item_status(action_item_id=action_item_id, status=payload.status.value)
        return APIResponse(success=True, message="Action item status updated.", data=updated)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Update failed: {e}")


@app.get("/api/v1/audit-logs", response_model=APIResponse, tags=["Audit Logs"])
async def get_audit_logs(
    limit: int = Query(50, ge=1, le=500),
    current_user: Dict[str, Any] = Depends(get_current_user),
):
    logs = fetch_user_audit_logs(user_id=current_user["id"], limit=limit)
    return APIResponse(success=True, message=f"Retrieved {len(logs)} audit log entries.", data=logs)


if __name__ == "__main__":
    log.info("Starting AI Meeting Assistance backend on http://0.0.0.0:8000")
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True, log_level="info")