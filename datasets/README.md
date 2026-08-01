# Datasets & Benchmarks (`datasets/`)

## Purpose
The `datasets` directory stores sample datasets, evaluation benchmarks, mock data payloads, and schemas for testing RAG indexing and AI agent performance.

## Responsibility
- Store open-source sample data files for testing domain plugins (such as Telecom protocol logs).
- Provide evaluation datasets for measuring RAG retrieval accuracy and agent tool-calling metrics.

## What Belongs Here
- Open-source, anonymized sample datasets (JSON, CSV, Parquet, Markdown).
- Synthetic benchmark logs and evaluation gold-standard files.

## What Does NOT Belong Here
- Proprietary enterprise data or PII (Personally Identifiable Information).
- Production database backups or raw binary databases.

## Future Roadmap
- Add sample Telecom RRC protocol log datasets for benchmark evaluation.
- Add evaluation schema specifications for RAG retrieval benchmarking.
