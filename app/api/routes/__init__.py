from app.api.routes.health import router as health_router
from app.api.routes.summarizer import router as summarizer_router

__all__ = ["health_router", "summarizer_router"]
