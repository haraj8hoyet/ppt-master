"""Slide outline generator using the OpenAI chat completion API."""

from __future__ import annotations

import json
import logging
from dataclasses import dataclass

from openai import OpenAI

from src.config import get_config

logger = logging.getLogger(__name__)


@dataclass
class Slide:
    title: str
    bullets: list[str]
    speaker_notes: str = ""


def _build_prompt(topic: str, num_slides: int) -> str:
    return (
        f"Create a {num_slides}-slide presentation outline about: {topic}.\n"
        "Return a JSON array where each element has keys: \'title\', \'bullets\' (list of strings), "
        "and \'speaker_notes\' (string). Return ONLY the JSON array, no markdown fences."
    )


def generate_outline(topic: str, num_slides: int | None = None) -> list[Slide]:
    """Call the LLM and return a list of Slide objects."""
    cfg = get_config()
    errors = cfg.validate()
    if errors:
        raise ValueError("Invalid configuration: " + "; ".join(errors))

    slides_count = min(num_slides or 10, cfg.max_slides)
    client = OpenAI(api_key=cfg.openai_api_key, base_url=cfg.openai_base_url)

    logger.info("Generating %d slides for topic: %s", slides_count, topic)
    response = client.chat.completions.create(
        model=cfg.openai_model,
        messages=[
            {"role": "system", "content": "You are a professional presentation designer."},
            {"role": "user", "content": _build_prompt(topic, slides_count)},
        ],
        temperature=0.7,
    )

    raw = response.choices[0].message.content or "[]"
    data: list[dict] = json.loads(raw)
    slides = [
        Slide(
            title=item.get("title", ""),
            bullets=item.get("bullets", []),
            speaker_notes=item.get("speaker_notes", ""),
        )
        for item in data
    ]
    logger.info("Received %d slides from LLM", len(slides))
    return slides
