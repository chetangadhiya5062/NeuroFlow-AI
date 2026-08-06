"""Factory for instantiating Knowledge Base repository implementations."""

from backend.knowledge_base.repository import (
    IKnowledgeBaseRepository,
    InMemoryKnowledgeBaseRepository,
)


class KnowledgeBaseRepositoryFactory:
    """Factory creating IKnowledgeBaseRepository instances based on configuration."""

    @staticmethod
    def create_repository(
        storage_type: str = "memory",
    ) -> IKnowledgeBaseRepository:
        """Instantiate target knowledge base repository adapter.

        Args:
            storage_type: Storage engine identifier string.

        Returns:
            Configured IKnowledgeBaseRepository instance.
        """
        return InMemoryKnowledgeBaseRepository()
