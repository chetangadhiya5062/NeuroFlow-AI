"""Master RAG Domain Service orchestrating document processing and retrieval."""

from typing import Any

from backend.core.types import Err, ErrorInfo, Ok, Result
from backend.knowledge_base import Document
from backend.rag.chunker import TextChunker
from backend.rag.embedding_service import EmbeddingService
from backend.rag.exceptions import RAGError
from backend.rag.pdf_parser import PDFParser
from backend.rag.retriever import RAGRetriever
from backend.rag.vector_storage import (
    IVectorStore,
    LocalVectorStorage,
    SearchResult,
    VectorRecord,
)


class RAGService:
    """Service orchestrating RAG document processing and retrieval."""

    def __init__(
        self,
        vector_store: IVectorStore | None = None,
        embedding_service: EmbeddingService | None = None,
        pdf_parser: PDFParser | None = None,
        chunker: TextChunker | None = None,
    ) -> None:
        """Initialize RAGService with component dependencies."""
        self.vector_store = vector_store or LocalVectorStorage()
        self.embedding_service = embedding_service or EmbeddingService()
        self.pdf_parser = pdf_parser or PDFParser()
        self.chunker = chunker or TextChunker()
        self.retriever = RAGRetriever(
            vector_store=self.vector_store,
            embedding_service=self.embedding_service,
        )

    async def process_and_index_document(
        self,
        document: Document,
        content: bytes,
    ) -> Result[int, ErrorInfo]:
        """Parse document bytes, chunk text, generate embeddings, and index.

        Args:
            document: Document aggregate instance.
            content: Raw document file bytes.

        Returns:
            Result wrapping count of indexed chunks or ErrorInfo.
        """
        try:
            # 1. Parse text from document content
            ext = document.metadata.file_extension
            raw_text = self.pdf_parser.parse_document(content, ext)

            if not raw_text or not raw_text.strip():
                return Ok(0)

            # 2. Chunk text
            meta = {
                "filename": document.metadata.filename,
                "mime_type": document.metadata.mime_type,
            }
            chunks = self.chunker.chunk_text(
                document_id=document.id.value,
                text=raw_text,
                extra_metadata=meta,
            )
            if not chunks:
                return Ok(0)

            # 3. Generate batch embeddings for chunks
            texts = [c.text for c in chunks]
            embeddings = await self.embedding_service.generate_batch_embeddings(
                texts
            )

            # 4. Construct VectorRecords
            records = [
                VectorRecord(
                    id=c.id.value,
                    document_id=document.id.value,
                    text=c.text,
                    embedding=emb,
                    metadata=c.metadata,
                )
                for c, emb in zip(chunks, embeddings, strict=True)
            ]

            # 5. Store in vector storage
            await self.vector_store.add_records(records)
            return Ok(len(records))
        except RAGError as exc:
            return Err(
                ErrorInfo(
                    message=exc.message,
                    error_code=exc.error_code,
                    details=exc.details,
                )
            )
        except Exception as exc:
            return Err(
                ErrorInfo(
                    message=f"RAG indexing failed: {exc}",
                    error_code="RAG_INDEXING_ERROR",
                )
            )

    async def retrieve_context(
        self,
        query: str,
        top_k: int = 3,
    ) -> Result[list[SearchResult], ErrorInfo]:
        """Retrieve top_k matching context chunks for user query prompt.

        Args:
            query: User query prompt string.
            top_k: Maximum chunk count.

        Returns:
            Result wrapping list of SearchResults.
        """
        try:
            matches = await self.retriever.retrieve_relevant_chunks(
                query=query, top_k=top_k
            )
            return Ok(matches)
        except RAGError as exc:
            return Err(
                ErrorInfo(
                    message=exc.message,
                    error_code=exc.error_code,
                    details=exc.details,
                )
            )
        except Exception as exc:
            return Err(
                ErrorInfo(
                    message=f"RAG retrieval failed: {exc}",
                    error_code="RAG_RETRIEVAL_ERROR",
                )
            )

    def format_sources(
        self, search_results: list[SearchResult]
    ) -> list[dict[str, Any]]:
        """Format SearchResult list into serializable JSON dictionary sources."""
        sources = []
        for match in search_results:
            rec = match.record
            sources.append(
                {
                    "document_id": rec.document_id,
                    "filename": rec.metadata.get("filename", "unknown"),
                    "text": rec.text,
                    "similarity_score": round(match.score, 4),
                }
            )
        return sources
