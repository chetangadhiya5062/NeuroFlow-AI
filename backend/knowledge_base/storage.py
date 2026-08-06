"""Local filesystem file storage adapter implementation."""

import asyncio
from pathlib import Path

from backend.knowledge_base.exceptions import StorageError


class LocalFileStorage:
    """Storage adapter persisting raw document files to local disk."""

    def __init__(self, base_directory: str = "./data/documents") -> None:
        """Initialize LocalFileStorage with target directory.

        Args:
            base_directory: Directory path for document storage.
        """
        self._base_dir = Path(base_directory)
        self._ensure_directory()

    def _ensure_directory(self) -> None:
        """Create target storage directory if absent."""
        try:
            self._base_dir.mkdir(parents=True, exist_ok=True)
        except Exception as exc:
            raise StorageError(
                f"Failed to create storage directory '{self._base_dir}': {exc}"
            ) from exc

    def _save_file_sync(
        self, document_id: str, filename: str, content: bytes
    ) -> str:
        """Synchronously write file bytes to local disk."""
        safe_filename = Path(filename).name
        target_path = self._base_dir / f"{document_id}_{safe_filename}"

        try:
            target_path.write_bytes(content)
            return str(target_path.resolve())
        except Exception as exc:
            raise StorageError(
                f"Failed to write document file to '{target_path}': {exc}"
            ) from exc

    async def save_file(
        self, document_id: str, filename: str, content: bytes
    ) -> str:
        """Save raw document bytes to local disk asynchronously.

        Args:
            document_id: Unique document EntityId string.
            filename: Original file name string.
            content: Raw byte content of file.

        Returns:
            Resolved absolute file path string.
        """
        return await asyncio.to_thread(
            self._save_file_sync, document_id, filename, content
        )

    def _read_file_sync(self, storage_path: str) -> bytes:
        """Synchronously read file bytes from disk."""
        path = Path(storage_path)
        if not path.exists():
            raise StorageError(f"File at path '{storage_path}' does not exist.")
        try:
            return path.read_bytes()
        except Exception as exc:
            raise StorageError(
                f"Failed to read file from '{storage_path}': {exc}"
            ) from exc

    async def read_file(self, storage_path: str) -> bytes:
        """Read document file bytes from local disk asynchronously."""
        return await asyncio.to_thread(self._read_file_sync, storage_path)

    def _delete_file_sync(self, storage_path: str) -> bool:
        """Synchronously delete file from disk."""
        path = Path(storage_path)
        if path.exists():
            try:
                path.unlink()
                return True
            except Exception as exc:
                raise StorageError(
                    f"Failed to delete file '{storage_path}': {exc}"
                ) from exc
        return False

    async def delete_file(self, storage_path: str) -> bool:
        """Delete document file from local disk asynchronously."""
        return await asyncio.to_thread(self._delete_file_sync, storage_path)
