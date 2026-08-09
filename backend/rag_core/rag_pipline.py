import os
import time
from agent.tools import set_session_transcript, set_active_session_id
from audio.audio_processor import AudioProcessor
from audio.transcribe import Transcriber
from rag_core.embedding import Embeddings
from rag_core.vector_db import VectorStore
from rag_core.chunking import Chunking
from utils.tools import Tools
from utils.logger import Logger
from database.meeting import insert_meeting, get_meeting_by_id


class RagPipeline:
    def __init__(self):
        self._audio_processor = AudioProcessor()
        self._transcriber = Transcriber()
        self._embedding = Embeddings()
        self._chunking = Chunking()
        self._tools = Tools()
        self._vector_store = VectorStore()
        self.log = Logger().get_logger()

    def load_existing_meeting_session(self, user_id: str, meeting_id: str) -> tuple[str, str]:
        meeting_meta = get_meeting_by_id(user_id=user_id, meeting_id=meeting_id)
        if meeting_meta:
            title = meeting_meta.get("title", meeting_id)
            pinecone_namespace = meeting_meta.get("pinecone_namespace") or meeting_id
        else:
            title = meeting_id
            pinecone_namespace = meeting_id

        session_id = f"{user_id}:{meeting_id}"

        set_active_session_id(session_id)
        set_session_transcript(
            chunks=[],
            embedding_vector=[],
            session_id=session_id,
            meeting_id=meeting_id,
            pinecone_namespace=pinecone_namespace,
            user_id=user_id,
        )

        self.log.info(f"Loaded cloud chat session '{session_id}' for '{title}'. Queries will target Pinecone namespace '{pinecone_namespace}'.")
        return meeting_id, title

    def rag_pipeline(self, url: str, user_id: str = "default_user", language: str = "english") -> tuple[str, str]:
        if not url:
            raise ValueError("No URL provided. Please provide a valid YouTube link or audio file path.")

        try:
            self.log.info(f"Processing audio/text source from {url}...")
            if os.path.exists(url) and url.endswith(".txt"):
                with open(url, "r", encoding="utf-8") as f:
                    content = f.read().strip()
                    full_transcript = content.replace("\r\n", "\n").replace("\n", " ").strip()


            else:
                audio_chunks = self._audio_processor.process_audio(url, language=language)
                self.log.info(f"Audio processing completed. Number of chunks: {len(audio_chunks)}")
                transcripts = self._transcriber.transcribe(audio_chunks, language=language)
                full_transcript = transcripts if isinstance(transcripts, str) else "\n".join(transcripts)

            self.log.info("Generating embeddings...")
            chunks = self._chunking.chunking(full_transcript, chunk_size=900, chunk_overlap=180)
            self.log.info(f"Total chunks created: {len(chunks)}")
            if not chunks:
                raise ValueError("Chunking produced 0 chunks — check the transcript content.")

            embedding_vector = self._embedding.embed_batch(chunks)
            self.log.info(f"Embeddings ready for {len(chunks)} chunks "
                          f"({len(embedding_vector[0])} dimensions).\n")

            meeting_id, title = self._tools.generate_meeting_id(full_transcript)
            session_id = f"{user_id}:{meeting_id}"

            set_active_session_id(session_id)
            set_session_transcript(
                chunks=chunks,
                embedding_vector=embedding_vector,
                session_id=session_id,
                meeting_id=meeting_id,
                pinecone_namespace=meeting_id,
                user_id=user_id,
            )

            try:
                self._vector_store.store_embeddings(meeting_id, chunks, embedding_vector)
                self.log.info(f"Embeddings and text stored in Pinecone Cloud under namespace '{meeting_id}'.\n")
            except Exception as e:
                self.log.warning(f"Could not persist meeting to Pinecone: {e}\n")

            try:
                insert_meeting(
                    meeting_id=meeting_id,
                    user_id=user_id,
                    title=title,
                    source_url=url,
                    pinecone_namespace=meeting_id,
                    language=language,
                    total_chunks=len(chunks),
                )
                self.log.info(f"Meeting metadata stored in Supabase database for user '{user_id}'.")
            except Exception as e:
                self.log.warning(f"Could not persist meeting metadata to Supabase: {e}")

            self.log.info("Session ready. The agent can now search, summarize, and answer questions.\n")
            return meeting_id, title
        except Exception as e:
            self.log.error(f"rag_pipeline failed: {e}")
            raise