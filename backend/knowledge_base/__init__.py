"""Knowledge Base subsystem for NeuroFlow AI."""

from backend.knowledge_base.document import Document
from backend.knowledge_base.exceptions import (
    DocumentNotFoundError,
    KnowledgeBaseError,
    StorageError,
    UnsupportedFormatError,
)
from backend.knowledge_base.metadata import DocumentMetadata
from backend.knowledge_base.parser import DocumentParser
from backend.knowledge_base.repository import (
    IKnowledgeBaseRepository,
    InMemoryKnowledgeBaseRepository,
)
from backend.knowledge_base.repository_factory import (
    KnowledgeBaseRepositoryFactory,
)
from backend.knowledge_base.service import KnowledgeBaseService
from backend.knowledge_base.storage import LocalFileStorage

__all__ = [
    "Document",
    "DocumentMetadata",
    "DocumentNotFoundError",
    "DocumentParser",
    "IKnowledgeBaseRepository",
    "InMemoryKnowledgeBaseRepository",
    "KnowledgeBaseError",
    "KnowledgeBaseRepositoryFactory",
    "KnowledgeBaseService",
    "LocalFileStorage",
    "StorageError",
    "UnsupportedFormatError",
]
