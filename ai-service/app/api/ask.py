from fastapi import APIRouter, Request

from app.core.config import get_settings
from app.core.logging import get_logger
from app.models.ask import AskRequest, AskResponse
from app.services.ai_service import AIService

settings = get_settings()

logger = get_logger(__name__)

router = APIRouter(
    prefix=settings.api_prefix,
    tags=["AI"],
)

ai_service = AIService()


@router.post(
    "/ask",
    response_model=AskResponse,
    summary="Ask OTMS AI Assistant",
    description="Send a natural language question to the OTMS AI Assistant.",
)
async def ask(
    request: Request,
    payload: AskRequest,
) -> AskResponse:

    logger.info("Received AI request.")

    answer = await ai_service.ask(
        http_client=request.app.state.http_client,
        question=payload.question,
    )

    logger.info("AI request completed successfully.")

    return AskResponse(answer=answer)