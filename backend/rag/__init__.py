"""RAG Subsystem for NeuroFlow AI."""

from backend.rag.chunker import DocumentChunk, TextChunker
from backend.rag.embedding_service import (
    EmbeddingService,
    IEmbeddingProvider,
    MockEmbeddingProvider,
)
from backend.rag.exceptions import (
    EmbeddingError,
    PDFParsingError,
    RAGError,
    VectorStorageError,
)
from backend.rag.pdf_parser import PDFParser
from backend.rag.rag_service import RAGService
from backend.rag.retriever import RAGRetriever
from backend.rag.vector_storage import (
    IVectorStore,
    LocalVectorStorage,
    SearchResult,
    VectorRecord,
)

__all__ = [
    "DocumentChunk",
    "EmbeddingError",
    "EmbeddingService",
    "IEmbeddingProvider",
    "IVectorStore",
    "LocalVectorStorage",
    "MockEmbeddingProvider",
    "PDFParser",
    "PDFParsingError",
    "RAGError",
    "RAGRetriever",
    "RAGService",
    "SearchResult",
    "TextChunker",
    "VectorRecord",
    "VectorStorageError",
]
