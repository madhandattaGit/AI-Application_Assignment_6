from fastapi import APIRouter

from app.schemas.summarizer import ErrorResponse, SummaryResponse, TextInput
from app.services import summarizer as summarizer_service

router = APIRouter(tags=["summarizer"])


@router.post(
    "/summarize",
    response_model=SummaryResponse,
    responses={
        422: {"model": ErrorResponse, "description": "Invalid request payload."},
        500: {"model": ErrorResponse, "description": "Unexpected server error."},
    },
)
def summarize(payload: TextInput) -> SummaryResponse:
    return SummaryResponse(summary=summarizer_service.summarize_text(payload.text))
