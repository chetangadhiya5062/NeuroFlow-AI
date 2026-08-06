"""Application bootstrap layer for NeuroFlow AI."""

from backend.app.application import create_app
from backend.app.bootstrap import bootstrap_platform
from backend.app.lifespan import platform_lifespan
from backend.app.shutdown import run_shutdown_tasks
from backend.app.startup import run_startup_tasks

__all__ = [
    "bootstrap_platform",
    "create_app",
    "platform_lifespan",
    "run_shutdown_tasks",
    "run_startup_tasks",
]
