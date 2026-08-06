"""Shared pytest configuration and fixtures for NeuroFlow AI test suite."""

from collections.abc import Generator

import pytest
from fastapi.testclient import TestClient

from backend.api.app import app
from backend.app.bootstrap import bootstrap_platform
from backend.config import ServiceContainer, Settings, get_settings


@pytest.fixture
def settings() -> Settings:
    """Fixture providing root application settings."""
    return get_settings()


@pytest.fixture
def container(settings: Settings) -> ServiceContainer:
    """Fixture providing initialized ServiceContainer."""
    c, _ = bootstrap_platform(settings=settings)
    return c


@pytest.fixture
def client() -> Generator[TestClient, None, None]:
    """Fixture providing TestClient with active platform lifespan."""
    with TestClient(app) as test_client:
        yield test_client
