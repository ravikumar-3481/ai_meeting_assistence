import datetime
from api.config import Config
from utils.logger import Logger
from rag_core.embedding import Embeddings
from pinecone import Pinecone, ServerlessSpec

EMBEDDING_DIMENSION = 384  # sentence-transformers/all-MiniLM-L6-v2


class VectorStore:
    def __init__(self):
        self.logger = Logger()
        self.log = self.logger.get_logger()
        self.config = Config()
        self._embedding = Embeddings()
        self._client = None
        self._index = None
        self._initialize_client()

    def _initialize_client(self) -> None:
        try:
            api_key = self.config.pinecone_api_key.get_secret_value()
            self._client = Pinecone(api_key=api_key)
            self._ensure_index_exists()
            self._index = self._client.Index(self.config.pinecone_index_name)
        except Exception as e:
            self.log.error(f"Failed to initialize Pinecone client: {e}")
            self._client = None
            self._index = None

    def _ensure_index_exists(self) -> None:
        index_name = self.config.pinecone_index_name
        existing_indexes = [idx["name"] for idx in self._client.list_indexes()]

        if index_name in existing_indexes:
            return

        self.log.info(f"Creating Pinecone index '{index_name}'...")
        self._client.create_index(
            name=index_name,
            dimension=EMBEDDING_DIMENSION,
            metric="cosine",
            spec=ServerlessSpec(
                cloud=self.config.pinecone_cloud,
                region=self.config.pinecone_region,
            ),
        )

    def _get_index(self):
        if self._index is None:
            raise RuntimeError(
                "Pinecone index is not available. Check your PINECONE_API_KEY "
                "and PINECONE_INDEX_NAME configuration."
            )
        return self._index

    def store_embeddings(
        self,
        meeting_id: str,
        chunks: list[str],
        embedding_vectors: list[list[float]],
        meeting_date: str | None = None,
    ) -> int:
        """
        Upsert a meeting's chunks + vectors into Pinecone under a namespace
        named after meeting_id. Returns the number of vectors stored.
        """
        if not meeting_id or not meeting_id.strip():
            raise ValueError("meeting_id is required to store embeddings")
        if not chunks or not embedding_vectors:
            self.log.warning(f"No chunks/vectors provided for meeting '{meeting_id}'")
            return 0
        if len(chunks) != len(embedding_vectors):
            raise ValueError("chunks and embedding_vectors must be the same length")

        date_tag = meeting_date or datetime.date.today().isoformat()

        vectors_to_upsert = []
        for i, (text, vector) in enumerate(zip(chunks, embedding_vectors)):
            if not text or not str(text).strip() or not vector:
                continue
            vectors_to_upsert.append({
                "id": f"{meeting_id}_chunk_{i}",
                "values": vector,
                "metadata": {
                    "meeting_id": meeting_id,
                    "date": date_tag,
                    "text": text,
                    "chunk_index": i,
                },
            })

        if not vectors_to_upsert:
            self.log.warning(f"All chunks empty/invalid for meeting '{meeting_id}', nothing stored")
            return 0

        try:
            index = self._get_index()
            index.upsert(vectors=vectors_to_upsert, namespace=meeting_id)
            self.log.info(
                f"Stored {len(vectors_to_upsert)} vectors for meeting "
                f"'{meeting_id}' in namespace '{meeting_id}'"
            )
            return len(vectors_to_upsert)
        except Exception as e:
            self.log.error(f"Failed to store embeddings for meeting '{meeting_id}': {e}")
            raise

    def list_meetings(self) -> list[str]:
        """Return every meeting_id (namespace) currently stored in the index."""
        try:
            index = self._get_index()
            stats = index.describe_index_stats()
            namespaces = stats.get("namespaces", {})
            return list(namespaces.keys())
        except Exception as e:
            self.log.error(f"Failed to list meetings: {e}")
            return []

    def query_cloud(
        self,
        question: str,
        top_k: int = 5,
        meeting_ids: list[str] | None = None,
    ) -> list[dict]:
        if not question or not question.strip():
            self.log.warning("Empty question passed to query_cloud")
            return []

        try:
            query_vector = self._embedding.embed_text(question)
        except Exception as e:
            self.log.error(f"Failed to embed query for query_cloud: {e}")
            return []

        if not query_vector:
            return []

        target_namespaces = meeting_ids if meeting_ids else self.list_meetings()
        if not target_namespaces:
            self.log.info("No meetings stored in Pinecone yet")
            return []

        index = self._get_index()
        all_matches = []

        for namespace in target_namespaces:
            try:
                response = index.query(
                    vector=query_vector,
                    top_k=top_k,
                    namespace=namespace,
                    include_metadata=True,
                )
                for match in response.get("matches", []):
                    metadata = match.get("metadata", {})
                    all_matches.append({
                        "meeting_id": metadata.get("meeting_id", namespace),
                        "date": metadata.get("date", "unknown_date"),
                        "text": metadata.get("text", ""),
                        "score": match.get("score", 0.0),
                    })
            except Exception as e:
                self.log.warning(f"Query failed for namespace '{namespace}': {e}")
                continue

        all_matches.sort(key=lambda item: item["score"], reverse=True)
        return all_matches[:top_k]

    def delete_meeting(self, meeting_id: str) -> bool:
        """Remove an entire meeting's vectors (its whole namespace) from Pinecone."""
        if not meeting_id or not meeting_id.strip():
            raise ValueError("meeting_id is required to delete a meeting")

        try:
            index = self._get_index()
            index.delete(delete_all=True, namespace=meeting_id)
            self.log.info(f"Deleted all vectors for meeting '{meeting_id}'")
            return True
        except Exception as e:
            self.log.error(f"Failed to delete meeting '{meeting_id}': {e}")
            return False