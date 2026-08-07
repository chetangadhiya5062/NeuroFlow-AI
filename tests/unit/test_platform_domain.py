"""Unit and API integration tests for multi-tenant Platform Domain hierarchy."""

import pytest
from fastapi.testclient import TestClient

from backend.api.app import get_application
from backend.platform_domain import (
    InMemoryProjectRepository,
    InMemoryUserRepository,
    InMemoryWorkspaceRepository,
    PlatformDomainService,
)


@pytest.mark.asyncio
async def test_platform_domain_hierarchy_service() -> None:
    """Test PlatformDomainService hierarchy."""
    user_repo = InMemoryUserRepository()
    ws_repo = InMemoryWorkspaceRepository()
    proj_repo = InMemoryProjectRepository()

    service = PlatformDomainService(
        user_repo=user_repo,
        workspace_repo=ws_repo,
        project_repo=proj_repo,
    )

    # 1. Create User
    user_res = await service.create_user(email="alice@corp.com", name="Alice Engineer")
    assert user_res.is_success
    user = user_res.unwrap()

    # 2. Create Workspace
    ws_res = await service.create_workspace(name="Engineering WS", owner_id=user.id)
    assert ws_res.is_success
    ws = ws_res.unwrap()
    assert ws.owner_id == user.id

    # 3. Create Project in Workspace
    proj_res = await service.create_project(
        workspace_id=ws.id,
        name="5G Telecom RAG",
        description="5G NR specification analysis project",
    )
    assert proj_res.is_success
    proj = proj_res.unwrap()
    assert proj.workspace_id == ws.id

    # 4. List Projects in Workspace
    list_res = await service.list_projects(workspace_id=ws.id)
    assert list_res.is_success
    projects = list_res.unwrap()
    assert len(projects) == 1
    assert projects[0].id == proj.id


def test_platform_domain_api_multi_tenant_flow() -> None:
    """Test end-to-end multi-tenant API workflow."""
    app = get_application()
    client = TestClient(app)

    # 1. Create Workspace
    ws_resp = client.post(
        "/workspaces",
        json={"name": "Acme Corp AI Workspace"},
    )
    assert ws_resp.status_code == 201
    ws_data = ws_resp.json()
    ws_id = ws_data["id"]
    assert ws_data["name"] == "Acme Corp AI Workspace"

    # 2. Create Project in Workspace
    proj_resp = client.post(
        f"/workspaces/{ws_id}/projects",
        json={
            "name": "Telecom Document Intelligence",
            "description": "3GPP Telecom Specifications Project",
        },
    )
    assert proj_resp.status_code == 201
    proj_data = proj_resp.json()
    proj_id = proj_data["id"]
    assert proj_data["workspace_id"] == ws_id

    # 3. List Projects in Workspace
    list_proj_resp = client.get(f"/workspaces/{ws_id}/projects")
    assert list_proj_resp.status_code == 200
    assert len(list_proj_resp.json()) >= 1

    # 4. Upload PDF Document into Project
    doc_content = (
        b"# Telecom Architecture\n"
        b"Radio Resource Control (RRC) Setup establishes initial connection "
        b"between User Equipment (UE) and gNodeB base station in 5G NR."
    )
    upload_resp = client.post(
        f"/projects/{proj_id}/documents/upload",
        files={
            "file": (
                "telecom.pdf",
                doc_content,
                "application/pdf",
            )
        },
    )
    assert upload_resp.status_code == 201
    assert upload_resp.json()["metadata"]["filename"] == "telecom.pdf"

    # 5. Ask Question via Chat API
    msg = "What does the uploaded telecom document say about RRC Setup?"
    chat_resp = client.post(
        "/chat",
        json={"message": msg},
    )
    assert chat_resp.status_code == 200
    chat_data = chat_resp.json()
    assert "response" in chat_data
