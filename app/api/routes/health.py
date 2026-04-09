from fastapi import APIRouter

from app.core.config import settings

router = APIRouter(tags=["health"])


@router.get("/")
def home() -> dict[str, str]:
    return {"message": f"{settings.app_name} is running"}
