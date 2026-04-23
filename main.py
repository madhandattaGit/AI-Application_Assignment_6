import logging
import re
from typing import Annotated

from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel, ConfigDict, Field

app = FastAPI()
logger = logging.getLogger(__name__)

# ✅ CORS Middleware (fixed syntax)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ Input schema
class TextInput(BaseModel):
    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)

    text: Annotated[str, Field(..., min_length=1, max_length=5000, strict=True)]

# ✅ Validation error handler
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

# ✅ Generic error handler
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

@app.get("/")
def home():
    return {"message": "NEW VERSION RUNNING"}

# ✅ Improved Summarization endpoint
@app.post("/summarize")
def summarize(input: TextInput):
    text = input.text.strip()
    words = text.split()

    # ✅ 1. Detect meaningless input
    if not re.search(r"[a-zA-Z]", text):
        return {"error": "Invalid input. Please enter meaningful text."}

    # ✅ 2. Handle very short input
    if len(words) < 5:
        return {
            "error": "Input too short. Please provide more detailed text."
        }

    # ✅ 3. Basic summarization logic
    if len(words) < 20:
        summary = text
    else:
        summary = " ".join(words[:20])

    # ✅ 4. Structured output (MAIN IMPROVEMENT)
    improved_summary = f"""
Key Summary:
{summary}

Key Insight:
- The text highlights important information. Review key points carefully.

Suggestion:
- Use this summary as a quick overview. Refer to full text for accuracy.
"""

    return {"summary": improved_summary}