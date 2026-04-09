from fastapi.testclient import TestClient

from summarizer_api.main import app
from summarizer_api.services import summarizer as summarizer_service

client = TestClient(app)


def test_home():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json()["message"] == "AI Summarizer API is running"


def test_summarize():
    response = client.post("/summarize", json={
        "text": "Artificial Intelligence is transforming industries worldwide by improving efficiency and decision making across multiple sectors."
    })

    assert response.status_code == 200
    assert "summary" in response.json()


def test_summarize_returns_original_text_when_input_has_exactly_twenty_words():
    text = "one two three four five six seven eight nine ten eleven twelve thirteen fourteen fifteen sixteen seventeen eighteen nineteen twenty"

    response = client.post("/summarize", json={"text": text})

    assert response.status_code == 200
    assert response.json() == {"summary": text}


def test_summarize_truncates_input_longer_than_twenty_words():
    text = (
        "one two three four five six seven eight nine ten eleven twelve thirteen "
        "fourteen fifteen sixteen seventeen eighteen nineteen twenty twentyone twentytwo"
    )

    response = client.post("/summarize", json={"text": text})

    assert response.status_code == 200
    assert response.json() == {
        "summary": (
            "one two three four five six seven eight nine ten eleven twelve thirteen "
            "fourteen fifteen sixteen seventeen eighteen nineteen twenty"
        )
    }


def test_summarize_strips_surrounding_whitespace_before_processing():
    response = client.post("/summarize", json={"text": "   concise input with padding   "})

    assert response.status_code == 200
    assert response.json() == {"summary": "concise input with padding"}


def test_summarize_rejects_whitespace_only_input():
    response = client.post("/summarize", json={"text": "   "})

    assert response.status_code == 422
    assert response.json()["error"] == "Invalid request payload"
    assert any("at least 1 character" in detail for detail in response.json()["details"])


def test_summarize_requires_text_field():
    response = client.post("/summarize", json={})

    assert response.status_code == 422
    assert response.json()["error"] == "Invalid request payload"
    assert any("Field required" in detail for detail in response.json()["details"])


def test_summarize_rejects_non_string_text():
    response = client.post("/summarize", json={"text": 123})

    assert response.status_code == 422
    assert response.json()["error"] == "Invalid request payload"
    assert any("valid string" in detail for detail in response.json()["details"])


def test_summarize_rejects_null_text():
    response = client.post("/summarize", json={"text": None})

    assert response.status_code == 422
    assert response.json()["error"] == "Invalid request payload"
    assert any("valid string" in detail for detail in response.json()["details"])


def test_summarize_rejects_array_payload_for_text():
    response = client.post("/summarize", json={"text": ["not", "a", "string"]})

    assert response.status_code == 422
    assert response.json()["error"] == "Invalid request payload"
    assert any("valid string" in detail for detail in response.json()["details"])


def test_summarize_rejects_unexpected_fields():
    response = client.post("/summarize", json={"text": "Valid text", "tone": "short"})

    assert response.status_code == 422
    assert response.json()["error"] == "Invalid request payload"
    assert any("Extra inputs are not permitted" in detail for detail in response.json()["details"])


def test_summarize_rejects_oversized_input():
    response = client.post("/summarize", json={"text": "w" * 5001})

    assert response.status_code == 422
    assert response.json()["error"] == "Invalid request payload"
    assert any("at most 5000 characters" in detail for detail in response.json()["details"])


def test_summarize_accepts_input_at_maximum_length_boundary():
    response = client.post("/summarize", json={"text": "w" * 5000})

    assert response.status_code == 200
    assert response.json() == {"summary": "w" * 5000}


def test_summarize_rejects_missing_request_body():
    response = client.post("/summarize")

    assert response.status_code == 422
    assert response.json()["error"] == "Invalid request payload"
    assert any("Field required" in detail for detail in response.json()["details"])


def test_summarize_rejects_malformed_json_body():
    response = client.post(
        "/summarize",
        content='{"text": "missing quote}',
        headers={"Content-Type": "application/json"},
    )

    assert response.status_code == 422
    assert response.json()["error"] == "Invalid request payload"
    assert any("JSON decode error" in detail for detail in response.json()["details"])


def test_summarize_returns_internal_server_error_for_unexpected_failures(monkeypatch):
    failing_client = TestClient(app, raise_server_exceptions=False)

    def boom(*args, **kwargs):
        raise RuntimeError("unexpected failure")

    monkeypatch.setattr(summarizer_service, "summarize_text", boom)

    response = failing_client.post("/summarize", json={"text": "Valid input"})

    assert response.status_code == 500
    assert response.json() == {
        "error": "Internal server error",
        "details": ["An unexpected error occurred while processing the request."],
    }
