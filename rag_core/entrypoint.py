from audio.audio_processor import AudioProcessor
from audio.transcribe import Transcriber
from rag_core.embedding import Embeddings
from rag_core.chunking import Chunking
from utils.logger import Logger
import time






class EntryPoint:
    def __init__(self):
        self._audio_processor = AudioProcessor()
        self._transcriber = Transcriber()
        self._embedding = Embeddings()
        self._chunking = Chunking()
        self.log = Logger().get_logger()

        
    def process_audio(self, url: str, language: str = "english") -> str:
        if not url:
            return "No URL provided. Please provide a valid YouTube link or audio file path."
        try:
            self.log.info(f"Processing audio from {url}...")
            audio_chunks = self._audio_processor.process_audio(url, language=language)
            self.log.info(f"Audio processing completed. Number of chunks: {len(audio_chunks)}")
            time.sleep(1)  # Simulate processing time
    
            self.log.info("Transcribing audio chunks...")
            transcripts = self._transcriber.transcribe(audio_chunks, language=language)
            time.sleep(1)  # Simulate processing time
    
            full_transcript = "\n".join(transcripts)
            self.log.info("Transcription completed. Generating embeddings...")
            text_chunks = self._chunking.chunking(full_transcript, chunk_size=900, chunk_overlap=180)
            time.sleep(1)  # Simulate processing time
    
            embedding_vector = self._embedding.embed_batch(text_chunks) 
            self.log.info(f"Embeddings generated for {len(text_chunks)} chunks.")
            time.sleep(1)  # Simulate processing time
    
            self.log.info(f"Embedding vector for first chunk: {len(embedding_vector[0])} dimensions")
            time.sleep(1)  # Simulate processing time
    
            return text_chunks, embedding_vector
        except Exception as e:
            self.log.error(f"process_audio failed: {e}")
            return f"Failed to process audio for {url}."