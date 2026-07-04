import google.generativeai as genai

from app.core.config import get_settings
from app.core.exceptions import ExternalServiceError
from app.core.logging_config import get_logger

logger = get_logger(__name__)

_model = None


class GeminiError(ExternalServiceError):
    """Raised when the Gemini API is misconfigured or a request fails."""


def _get_model():
    """Configure the Gemini client and load the model once, then reuse it."""
    global _model
    if _model is None:
        settings = get_settings()

        if not settings.google_api_key:
            raise GeminiError("GOOGLE_API_KEY is not set in the environment.")

        genai.configure(api_key=settings.google_api_key)
        logger.info("Initializing Gemini model: %s", settings.gemini_model)
        _model = genai.GenerativeModel(settings.gemini_model)

    return _model


def generate_answer(prompt: str) -> str:
    """Send a prompt to Gemini and return the generated text response."""
    model = _get_model()

    try:
        response = model.generate_content(prompt)
    except Exception as exc:
        logger.exception("Gemini API call failed")
        raise GeminiError(f"Failed to generate a response from Gemini: {exc}") from exc

    if not response.text:
        raise GeminiError("Gemini returned an empty response.")

    logger.info("Generated response from Gemini (%d characters)", len(response.text))
    return response.text.strip()