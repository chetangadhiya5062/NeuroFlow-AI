"""SQLite conversation repository adapter implementation."""

import asyncio
import json
import sqlite3
import threading
from collections.abc import Generator
from contextlib import contextmanager
from datetime import datetime
from pathlib import Path

from backend.conversation.conversation import Conversation
from backend.conversation.message import Message
from backend.conversation.models import MessageRole
from backend.conversation.repository import IConversationRepository
from backend.core.value_objects import EntityId, TenantId, Timestamp


class SQLiteConversationRepository(IConversationRepository):
    """Thread-safe SQLite conversation repository implementation."""

    def __init__(self, db_path: str = "./data/conversations.db") -> None:
        """Initialize SQLite repository and create schema if absent.

        Args:
            db_path: Path to SQLite database file.
        """
        self._db_path = db_path
        self._lock = threading.RLock()
        self._init_db()

    @contextmanager
    def _get_connection(self) -> Generator[sqlite3.Connection, None, None]:
        """Create, yield, and close a sqlite3 connection."""
        conn = sqlite3.connect(self._db_path)
        conn.row_factory = sqlite3.Row
        try:
            yield conn
        finally:
            conn.close()

    def _init_db(self) -> None:
        """Create database directory and table schemas if absent."""
        db_dir = Path(self._db_path).parent
        db_dir.mkdir(parents=True, exist_ok=True)

        with self._lock, self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS conversations (
                    id TEXT PRIMARY KEY,
                    tenant_id TEXT,
                    title TEXT,
                    metadata TEXT NOT NULL,
                    created_at TEXT NOT NULL,
                    updated_at TEXT NOT NULL
                );
                """
            )
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS messages (
                    id TEXT PRIMARY KEY,
                    conversation_id TEXT NOT NULL,
                    role TEXT NOT NULL,
                    content TEXT NOT NULL,
                    metadata TEXT NOT NULL,
                    created_at TEXT NOT NULL,
                    FOREIGN KEY (conversation_id)
                        REFERENCES conversations (id) ON DELETE CASCADE
                );
                """
            )
            conn.commit()

    def _save_sync(self, conversation: Conversation) -> None:
        """Synchronously persist conversation aggregate and messages."""
        with self._lock, self._get_connection() as conn:
            cursor = conn.cursor()
            # 1. Upsert conversation
            tenant_val = (
                conversation.tenant_id.value
                if conversation.tenant_id
                else None
            )
            cursor.execute(
                """
                INSERT INTO conversations
                    (id, tenant_id, title, metadata, created_at, updated_at)
                VALUES (?, ?, ?, ?, ?, ?)
                ON CONFLICT(id) DO UPDATE SET
                    tenant_id=excluded.tenant_id,
                    title=excluded.title,
                    metadata=excluded.metadata,
                    updated_at=excluded.updated_at;
                """,
                (
                    conversation.id.value,
                    tenant_val,
                    conversation.title,
                    json.dumps(conversation.metadata),
                    conversation.created_at.value.isoformat(),
                    conversation.updated_at.value.isoformat(),
                ),
            )

            # 2. Replace messages for this conversation
            cursor.execute(
                "DELETE FROM messages WHERE conversation_id = ?;",
                (conversation.id.value,),
            )

            for msg in conversation.messages:
                cursor.execute(
                    """
                    INSERT INTO messages
                        (id, conversation_id, role, content, metadata, created_at)
                    VALUES (?, ?, ?, ?, ?, ?);
                    """,
                    (
                        msg.id.value,
                        conversation.id.value,
                        msg.role.value,
                        msg.content,
                        json.dumps(msg.metadata),
                        msg.created_at.value.isoformat(),
                    ),
                )

            conn.commit()

    async def save(self, conversation: Conversation) -> None:
        """Save or update conversation aggregate asynchronously."""
        await asyncio.to_thread(self._save_sync, conversation)

    def _get_by_id_sync(self, conversation_id: EntityId) -> Conversation | None:
        """Synchronously fetch conversation aggregate by EntityId."""
        with self._lock, self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT * FROM conversations WHERE id = ?;",
                (conversation_id.value,),
            )
            row = cursor.fetchone()
            if row is None:
                return None

            tenant_id = (
                TenantId(row["tenant_id"]) if row["tenant_id"] else None
            )
            cid = EntityId(row["id"])
            created_at = Timestamp(
                value=datetime.fromisoformat(row["created_at"])
            )
            updated_at = Timestamp(
                value=datetime.fromisoformat(row["updated_at"])
            )

            # Fetch messages
            cursor.execute(
                "SELECT * FROM messages WHERE conversation_id = ? "
                "ORDER BY created_at ASC;",
                (conversation_id.value,),
            )
            msg_rows = cursor.fetchall()
            messages = []
            for mrow in msg_rows:
                messages.append(
                    Message(
                        id=EntityId(mrow["id"]),
                        role=MessageRole(mrow["role"]),
                        content=mrow["content"],
                        metadata=json.loads(mrow["metadata"]),
                        created_at=Timestamp(
                            value=datetime.fromisoformat(mrow["created_at"])
                        ),
                    )
                )

            return Conversation(
                id=cid,
                tenant_id=tenant_id,
                title=row["title"],
                messages=messages,
                metadata=json.loads(row["metadata"]),
                created_at=created_at,
                updated_at=updated_at,
            )

    async def get_by_id(self, conversation_id: EntityId) -> Conversation | None:
        """Get conversation by EntityId asynchronously."""
        return await asyncio.to_thread(self._get_by_id_sync, conversation_id)

    def _delete_sync(self, conversation_id: EntityId) -> bool:
        """Synchronously delete conversation and messages."""
        with self._lock, self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "DELETE FROM messages WHERE conversation_id = ?;",
                (conversation_id.value,),
            )
            cursor.execute(
                "DELETE FROM conversations WHERE id = ?;",
                (conversation_id.value,),
            )
            conn.commit()
            return cursor.rowcount > 0

    async def delete(self, conversation_id: EntityId) -> bool:
        """Delete conversation by EntityId asynchronously."""
        return await asyncio.to_thread(self._delete_sync, conversation_id)

    def _list_conversations_sync(
        self, tenant_id: TenantId | None, limit: int
    ) -> list[Conversation]:
        """Synchronously list stored conversations."""
        with self._lock, self._get_connection() as conn:
            cursor = conn.cursor()
            if tenant_id is not None:
                cursor.execute(
                    "SELECT id FROM conversations WHERE tenant_id = ? LIMIT ?;",
                    (tenant_id.value, limit),
                )
            else:
                cursor.execute(
                    "SELECT id FROM conversations LIMIT ?;", (limit,)
                )

            rows = cursor.fetchall()
            results = []
            for row in rows:
                conv = self._get_by_id_sync(EntityId(row["id"]))
                if conv is not None:
                    results.append(conv)
            return results

    async def list_conversations(
        self, tenant_id: TenantId | None = None, limit: int = 50
    ) -> list[Conversation]:
        """List stored conversations up to limit asynchronously."""
        return await asyncio.to_thread(
            self._list_conversations_sync, tenant_id, limit
        )
