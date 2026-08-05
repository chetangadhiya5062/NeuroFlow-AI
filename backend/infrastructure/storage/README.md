<!--
File: backend/infrastructure/storage/README.md
Project: NeuroFlow AI
-->

# Infrastructure Storage Package (`backend/infrastructure/storage/`)

## Purpose
Provides S3, Azure Blob, and local filesystem storage adapters implementing `IStoragePort` and `ICheckpointStorePort`.

## Responsibilities
- Implement `IStoragePort` for document binary storage, blob retrieval, and presigned URL generation.
- Implement `ICheckpointStorePort` for workflow execution state snapshots.

## Public Interfaces
- `S3StorageAdapter`, `AzureBlobStorageAdapter`, `LocalStorageAdapter`

## Allowed Dependencies
- Python standard library (`typing`, `pathlib`).
- Layer 0 Core contracts (`backend/core/ports/`, `backend/core/exceptions/`).
- Storage SDKs (`boto3`, `azure-storage-blob`).

## Forbidden Dependencies
- Layer 3 Platform Runtimes (`backend/knowledge_base/`, `backend/workflow_engine/`).

## Related Documents
- `docs/architecture/knowledge-base.md`
- `docs/architecture/workflow-engine.md`

## Current Status
Scaffolded — Storage adapters to be implemented in Milestone 2.
