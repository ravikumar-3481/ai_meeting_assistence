from logging import log

from agent.tools import set_session_transcript
from audio.audio_processor import AudioProcessor
from audio.transcribe import Transcriber
from main import TRANSCRIPT_PATH
from rag_core import chunking
from rag_core.embedding import Embeddings
from rag_core.vector_db import VectorStore
from rag_core.chunking import Chunking
from utils.tools import Tools
from utils.logger import Logger
import time


class RagPipeline:
    def __init__(self):
        self._audio_processor = AudioProcessor()
        self._transcriber = Transcriber()
        self._embedding = Embeddings()
        self._chunking = Chunking()
        self._tools = Tools()
        self._vector_store = VectorStore()
        self.log = Logger().get_logger()

    def rag_pipeline(self, url: str, language: str = "english") -> str:
        if not url:
            return "No URL provided. Please provide a valid YouTube link or audio file path."
        try:
            # Process the audio and return audio chunks
            self.log.info(f"Processing audio from {url}...")
            audio_chunks = self._audio_processor.process_audio(url, language=language)
            self.log.info(f"Audio processing completed. Number of chunks: {len(audio_chunks)}")
            time.sleep(1)  

            # Transcribe the audio chunks and return transcripts
            self.log.info("Transcribing audio chunks...")
            transcripts = self._transcriber.transcribe(audio_chunks, language=language)
            full_transcript = "\n".join(transcripts)
            self.log.info("Transcription completed. Generating embeddings...")
            time.sleep(1) 

            # Chunk the transcript and generate embeddings
            chunks = self._chunking.chunking(full_transcript, chunk_size=900, chunk_overlap=180)
            self.log.info(f"Total chunks created: {len(chunks)}")
            if not chunks:
                raise ValueError("Chunking produced 0 chunks — check the transcript content.")

            # Generate embeddings for the chunks
            embedding_vector = self._embedding.embed_batch(chunks)
            self.log.info(f"Embeddings ready for {len(chunks)} chunks "
                          f"({len(embedding_vector[0])} dimensions).\n")

            set_session_transcript(chunks, embedding_vector)
            
            # generate a unique meeting ID and store the embeddings in Pinecone
            meeting_id , title = self._tools.generate_meeting_id(full_transcript)
            try:
                # store the embeddings in Pinecone database
                self._vector_store.store_embeddings(meeting_id, chunks, embedding_vector)
                self.log.info(f"Meeting stored in Pinecone as '{meeting_id}'.\n")
            except Exception as e:
                self.log.warning(f"Could not persist meeting to Pinecone: {e}\n")
        
            self.log.info("Session ready. The agent can now search, summarize, and generate "
                          "action items / minutes / follow-up emails for this meeting.\n")

            # return unique meeting id
            return meeting_id , title
        except Exception as e:
            self.log.error(f"rag_pipeline failed: {e}")
            return f"Failed to process audio for {url}."