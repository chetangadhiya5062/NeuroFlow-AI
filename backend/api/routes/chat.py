"""Chat completion API ingress router."""

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field

from backend.config import ServiceContainer, get_container
from backend.services.chat_service import ChatService


class ChatRequest(BaseModel):
    """Chat request payload model."""

    message: str = Field(
        ...,
        description="User message prompt text",
        examples=["Hello"],
    )


class ChatResponse(BaseModel):
    """Chat response payload model."""

    response: str = Field(
        ...,
        description="Generated AI response text",
        examples=["Hello from NeuroFlow AI Mock Provider"],
    )


router = APIRouter(tags=["Chat"])


def get_chat_service(
    container: ServiceContainer = Depends(get_container),  # noqa: B008
) -> ChatService:
    """Dependency resolver for ChatService."""
    return container.resolve(ChatService)


@router.post("/chat", response_model=ChatResponse)
async def post_chat(
    payload: ChatRequest,
    chat_service: ChatService = Depends(get_chat_service),  # noqa: B008
) -> ChatResponse:
    """Execute end-to-end chat generation flow via LLM Gateway and Mock Provider.

    Args:
        payload: ChatRequest JSON body containing user message.
        chat_service: Injected ChatService instance.

    Returns:
        ChatResponse JSON object containing AI response.

    Raises:
        HTTPException: If chat processing fails.
    """
    result = await chat_service.process_chat(payload.message)
    if result.is_success:
        return ChatResponse(response=result.unwrap())

    error_info = result.unwrap_err()
    raise HTTPException(
        status_code=400 if error_info.error_code == "VALIDATION_ERROR" else 500,
        detail=error_info.message,
    )
