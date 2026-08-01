# Backend - RAG Subsystem (`backend/rag`)

## Purpose
The `rag` module contains Retrieval-Augmented Generation capabilities, managing knowledge ingestion, embedding generation, index construction, and semantic retrieval pipelines.

## Responsibility
- Parse, extract, and chunk documents and data sources.
- Generate vector embeddings via specialized embedding models.
- Build and maintain vector index databases.
- Retrieve and rerank context passages relevant to user queries.

## Subdirectory Structure
- **`ingestion/`**: Data connectors, document parsers, and text chunking strategies.
- **`embeddings/`**: Embedding model wrappers and batch vectorization engine.
- **`retrieval/`**: Hybrid search, vector similarity search, and reranking algorithms.
- **`indexing/`**: Vector database client interfaces, index updates, and metadata management.

## What Belongs Here
- Chunking, parsing, and text extraction logic.
- Embedding provider adapters and vector store interfaces.
- Reranking algorithms and hybrid dense/sparse search logic.

## What Does NOT Belong Here
- Base LLM provider calls (belongs in `backend/ai/`).
- Web API endpoints or frontend UI components.

## Future Roadmap
- Support for hybrid BM25 + dense vector retrieval.
- Multi-vector document indexers and contextual compression retrievers.
