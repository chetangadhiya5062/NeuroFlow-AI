"""RAG Context Retriever implementation."""

from backend.rag.embedding_service import EmbeddingService
from backend.rag.vector_storage import IVectorStore, SearchResult


class RAGRetriever:
    """Retriever searching vector storage for relevant context chunks."""

    def __init__(
        self,
        vector_store: IVectorStore,
        embedding_service: EmbeddingService,
    ) -> None:
        """Initialize RAGRetriever with vector store and embedding service.

        Args:
            vector_store: IVectorStore interface implementation.
            embedding_service: EmbeddingService instance.
        """
        self._vector_store = vector_store
        self._embedding_service = embedding_service

    async def retrieve_relevant_chunks(
        self, query: str, top_k: int = 3
    ) -> list[SearchResult]:
        """Generate query embedding and retrieve top_k matching chunks.

        Args:
            query: User query prompt string.
            top_k: Maximum number of relevant chunks to retrieve.

        Returns:
            List of SearchResult objects containing matches and scores.
        """
        if not query or not query.strip():
            return []

        query_embedding = await self._embedding_service.generate_embedding(query)
        return await self._vector_store.search(query_embedding, top_k=top_k)
