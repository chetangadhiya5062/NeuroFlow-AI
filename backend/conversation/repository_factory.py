"""Factory for instantiating conversation repository implementations."""

from backend.conversation.adapters.memory_repository import (
    InMemoryConversationRepository,
)
from backend.conversation.adapters.sqlite_repository import (
    SQLiteConversationRepository,
)
from backend.conversation.repository import IConversationRepository


class ConversationRepositoryFactory:
    """Factory creating IConversationRepository instances based on configuration."""

    @staticmethod
    def create_repository(
        storage_type: str = "memory",
        sqlite_db_path: str = "./data/conversations.db",
    ) -> IConversationRepository:
        """Instantiate target conversation repository adapter.

        Args:
            storage_type: Storage engine type string ('memory', 'sqlite').
            sqlite_db_path: Target SQLite database file path.

        Returns:
            Configured IConversationRepository instance.
        """
        stype = storage_type.lower()
        if stype == "sqlite":
            return SQLiteConversationRepository(db_path=sqlite_db_path)

        return InMemoryConversationRepository()
