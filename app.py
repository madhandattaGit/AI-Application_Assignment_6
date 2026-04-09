import logging
from typing import Annotated

from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel, ConfigDict, Field

app = FastAPI()
logger = logging.getLogger(__name__)

# ✅ CORS configuration (IMPORTANT for frontend communication)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://127.0.0.1:5500"],  # Live Server URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ Input schema
class TextInput(BaseModel):
    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)

    text: Annotated[str, Field(..., min_length=1, max_length=5000, strict=True)]


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(_, exc: RequestValidationError):
    details = [
        f"{'.'.join(str(part) for part in error['loc'] if part != 'body')}: {error['msg']}"
        if any(part != "body" for part in error["loc"])
        else error["msg"]
        for error in exc.errors()
    ]
    return JSONResponse(
        status_code=422,
        content={"error": "Invalid request payload", "details": details},
    )


@app.exception_handler(Exception)
async def unhandled_exception_handler(_, exc: Exception):
    logger.exception("Unhandled application error", exc_info=exc)
    return JSONResponse(
        status_code=500,
        content={
            "error": "Internal server error",
            "details": ["An unexpected error occurred while processing the request."],
        },
    )

# ✅ Root endpoint
@app.get("/")
def home():
    return {"message": "AI Summarizer API is running"}

# ✅ Summarization endpoint
@app.post("/summarize")
def summarize(input: TextInput):
    words = input.text.split()

    # ✅ Validation (added using Codex suggestion)


    # ✅ Simple summarization logic
    if len(words) < 20:
        summary = input.text
    else:
        summary = " ".join(words[:20])

    return {"summary": summary}
