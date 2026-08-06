import time
import numpy as np
from api.config import Config
from utils.logger import Logger
from rag_core.chunking import Chunking
from huggingface_hub import InferenceClient
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn, TaskProgressColumn
from sklearn.metrics.pairwise import cosine_similarity


chunks = Chunking()


class Embeddings:
    def __init__(self):
        self.logger = Logger()
        self.log = self.logger.get_logger()
        self.model_name = "sentence-transformers/all-MiniLM-L6-v2"
        self.client = None
        self._initialize_client()

    def _initialize_client(self):
        try:
            self.client = InferenceClient(
                provider="hf-inference",
                api_key=Config().huggingface_api_token.get_secret_value()
            )
        except Exception as exc:
            self.log.warning(f"Inference client could not be initialized: {exc}")
            self.client = None

    def _get_client(self):
        if self.client is None:
            self._initialize_client()
        if self.client is None:
            raise RuntimeError("Inference client is not available. Check your Hugging Face token configuration.")
        return self.client

    def embed_text(self, text: str, retries: int = 2) -> list:
        if not text or not text.strip():
            self.log.warning("Empty text passed for embedding")
            return []

        for attempt in range(retries + 1):
            try:
                client = self._get_client()
                result = client.feature_extraction(text, model=self.model_name)
                return result.tolist() if hasattr(result, "tolist") else result
            except Exception as e:
                if attempt < retries:
                    self.log.warning(f"Embedding attempt {attempt + 1} failed, retrying: {e}")
                    time.sleep(2)
                else:
                    self.log.error(f"Embedding failed after {retries + 1} attempts: {e}")
                    raise RuntimeError(f"Failed to generate embedding: {e}") from e

    
    def embed_batch(self, texts: list) -> list:
        if not texts:
            return []
    
        embeddings = []
    
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            BarColumn(),
            TaskProgressColumn(),
        ) as progress:
            
            # Add task for tracking batch embedding
            task = progress.add_task("[yellow]Generating embeddings...", total=len(texts))
    
            for i, text in enumerate(texts):
                progress.update(task, description=f"[cyan]Embedding chunk {i + 1}/{len(texts)}...")
    
                if not text or not str(text).strip():
                    self.log.warning(f"Skipping empty chunk at index {i}")
                    embeddings.append([])
                    progress.advance(task)
                    continue
    
                embeddings.append(self.embed_text(text))
                progress.advance(task)
    
        return embeddings

    def _cosine_similarity(self, query_vector: list | np.ndarray, chunk_vector: list | np.ndarray) -> float:
        query_array = np.asarray(query_vector, dtype=float).reshape(1, -1)
        chunk_array = np.asarray(chunk_vector, dtype=float).reshape(1, -1)

        if query_array.size == 0 or chunk_array.size == 0:
            return 0.0

        similarity = cosine_similarity(query_array, chunk_array)[0][0]
        return float(similarity)

    def search_relevant_chunks(
        self,
        question: str,
        chunk_texts: list[str] | None = None,
        embedding_vectors: list[list[float]] | None = None,
        top_k: int = 3,
        query_embedding: list[float] | np.ndarray | None = None,
    ) -> list[dict]:
        
        if not question or not str(question).strip():
            self.log.warning("Empty question passed for chunk search")
            return []

        if top_k <= 0:
            return []

        if chunk_texts is None:
            raise ValueError("chunk_texts must be provided")
        if not chunk_texts:
            return []

        if embedding_vectors is None:
            embedding_vectors = self.embed_batch(chunk_texts)

        if len(chunk_texts) != len(embedding_vectors):
            raise ValueError("chunk_texts and embedding_vectors must contain the same number of items")

        if query_embedding is None:
            query_embedding = self.embed_text(question)
        query_embedding = np.asarray(query_embedding, dtype=float).reshape(1, -1)

        if query_embedding.size == 0:
            return []

        chunk_matrix = np.asarray(embedding_vectors, dtype=float)
        if chunk_matrix.ndim != 2:
            raise ValueError("embedding_vectors must be a 2D array-like structure")
        if chunk_matrix.shape[1] != query_embedding.shape[1]:
            raise ValueError("Query embedding and chunk embeddings must have the same dimensionality")

        scores = cosine_similarity(query_embedding, chunk_matrix)[0]
        ranked_chunks = []
        for index, (text, score) in enumerate(zip(chunk_texts, scores)):
            if not text or not str(text).strip():
                continue
            ranked_chunks.append({"index": index, "text": text, "score": float(score)})

        ranked_chunks.sort(key=lambda item: item["score"], reverse=True)
        return ranked_chunks[:top_k]



    def get_context(self, question: str, chunk_texts: list[str], embedding_vectors: list[list[float]], top_k: int = 3) -> str:
        relevant_chunks = self.search_relevant_chunks(
            question=question,
            chunk_texts=chunk_texts,
            embedding_vectors=embedding_vectors,
            top_k=top_k
        )

        self.log.info(f"Top {len(relevant_chunks)} relevant chunks for the question '{question}':\n")
        for i, result in enumerate(relevant_chunks):
            self.log.info(f"Rank {i + 1}: Score: {result['score']:.4f}, Text: {result['text']}...\n")

        return " ".join([chunk["text"] for chunk in relevant_chunks])
