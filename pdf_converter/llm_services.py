"""Custom Marker LLM services with additional logging."""

from __future__ import annotations

import logging
from typing import List

from marker.schema import Block  # type: ignore
from marker.services.gemini import GoogleGeminiService  # type: ignore
from pydantic import BaseModel  # type: ignore

try:
    from PIL import Image  # type: ignore
except Exception:  # pragma: no cover - optional dependency is part of marker
    Image = object  # type: ignore

LOG = logging.getLogger("pdf_converter.llm")
_PROMPT_PREVIEW_LEN = 2000


class LoggingGoogleGeminiService(GoogleGeminiService):
    """Google Gemini service that logs prompts before delegating to Marker."""

    def __call__(
        self,
        prompt: str,
        image: Image | List[Image] | None,
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
