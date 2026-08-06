"""Unit tests for conversation repository adapters and factory."""

import os
import tempfile

import pytest

from backend.conversation import (
    Conversation,
    ConversationRepositoryFactory,
    InMemoryConversationRepository,
    MessageRole,
    SQLiteConversationRepository,
)


@pytest.mark.asyncio
async def test_memory_repository_lifecycle() -> None:
    """Test InMemoryConversationRepository save, get, and list operations."""
    repo = InMemoryConversationRepository()
    conv = Conversation.create(title="Memory Test")
    conv.add_message(role=MessageRole.USER, content="Hello Memory")

    await repo.save(conv)
    retrieved = await repo.get_by_id(conv.id)
    assert retrieved is not None
    assert retrieved.title == "Memory Test"
    assert len(retrieved.messages) == 1
    assert retrieved.messages[0].content == "Hello Memory"


@pytest.mark.asyncio
async def test_sqlite_repository_persistence_and_restart() -> None:
    """Test SQLiteConversationRepository persists data across re-instantiation."""
    with tempfile.TemporaryDirectory() as tmp_dir:
        db_path = os.path.join(tmp_dir, "test_conv.db")

        # 1. First instantiation and save
        repo1 = SQLiteConversationRepository(db_path=db_path)
        conv = Conversation.create(title="SQLite Persisted Session")
        conv.add_message(role=MessageRole.USER, content="Persistent prompt")
        conv.add_message(role=MessageRole.ASSISTANT, content="Persistent response")
        await repo1.save(conv)

        cid = conv.id

        # 2. Simulate server restart with second instantiation accessing same DB file
        repo2 = SQLiteConversationRepository(db_path=db_path)
        restarted_conv = await repo2.get_by_id(cid)

        assert restarted_conv is not None
        assert restarted_conv.title == "SQLite Persisted Session"
        history = restarted_conv.get_history()
        assert len(history) == 2
        assert history[0].role == MessageRole.USER
        assert history[0].content == "Persistent prompt"
        assert history[1].role == MessageRole.ASSISTANT
        assert history[1].content == "Persistent response"


def test_repository_factory() -> None:
    """Test ConversationRepositoryFactory constructs correct repository adapter."""
    mem_repo = ConversationRepositoryFactory.create_repository(storage_type="memory")
    assert isinstance(mem_repo, InMemoryConversationRepository)

    with tempfile.TemporaryDirectory() as tmp_dir:
        db_path = os.path.join(tmp_dir, "factory.db")
        sql_repo = ConversationRepositoryFactory.create_repository(
            storage_type="sqlite", sqlite_db_path=db_path
        )
        assert isinstance(sql_repo, SQLiteConversationRepository)
