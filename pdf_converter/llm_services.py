"""Custom Marker LLM services with additional logging."""

import logging
from marker.schema.blocks import Block  # type: ignore
from marker.services.gemini import GoogleGeminiService  # type: ignore
from pydantic import BaseModel  # type: ignore

from PIL.Image import Image as PILImage

LOG = logging.getLogger("pdf_converter.llm")
_PROMPT_PREVIEW_LEN = 2000


class LoggingGoogleGeminiService(GoogleGeminiService):
    """Google Gemini service that logs prompts before delegating to Marker."""

    def __call__(
        self,
        prompt: str,
        image: PILImage | list[PILImage] | None,
        block: Block | None,
        response_schema: type[BaseModel],
        max_retries: int | None = None,
        timeout: int | None = None,
    ):
        preview = prompt[:_PROMPT_PREVIEW_LEN]
        truncated = "" if len(prompt) <= _PROMPT_PREVIEW_LEN else " …(truncated)"
        LOG.info("Gemini prompt (%d chars)%s:\n%s", len(prompt), truncated, preview)
        if image:
            if isinstance(image, list):
                LOG.info("Gemini prompt includes %d image(s).", len(image))
            else:
                LOG.info("Gemini prompt includes 1 image.")
        return super().__call__(
            prompt,
            image,
            block,
            response_schema,
            max_retries=max_retries,
            timeout=timeout,
        )


__all__ = ["LoggingGoogleGeminiService"]
