"""API routes for Chat completion execution."""

from typing import Any

from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel

from backend.config import get_container
from backend.services.chat_service import ChatService

router = APIRouter(prefix="/chat", tags=["Chat"])


class ChatRequest(BaseModel):
    """Chat API request payload schema."""

    message: str
    conversation_id: str | None = None


class ChatResponse(BaseModel):
    """Chat API response payload schema."""

    response: str
    conversation_id: str
    model: str
    provider: str
    sources: list[dict[str, Any]] = []


@router.post("", response_model=ChatResponse, status_code=status.HTTP_200_OK)
async def chat_completion(request: ChatRequest) -> ChatResponse:
    """Execute AI chat completion via AI Request Pipeline."""
    container = get_container()
    service = container.resolve(ChatService)

    result = await service.process_chat_full(
        message=request.message,
        conversation_id=request.conversation_id,
    )

    if not result.is_success:
        err = result.unwrap_err()
        status_code = (
            status.HTTP_400_BAD_REQUEST
            if err.error_code == "VALIDATION_ERROR"
            else status.HTTP_500_INTERNAL_SERVER_ERROR
        )
        raise HTTPException(status_code=status_code, detail=err.message)

    pipeline_res = result.unwrap()
    sources = pipeline_res.metadata.get("sources", [])

    return ChatResponse(
        response=pipeline_res.content,
        conversation_id=pipeline_res.conversation_id,
        model=pipeline_res.model_used,
        provider=pipeline_res.provider_used,
        sources=sources,
    )
