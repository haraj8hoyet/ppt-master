"""Tests for src/slide_generator.py."""

import json
from unittest.mock import MagicMock, patch

import pytest

from src.slide_generator import Slide, _build_prompt, generate_outline


SAMPLE_SLIDES = [
    {"title": "Intro", "bullets": ["Point A", "Point B"], "speaker_notes": "Welcome!"},
    {"title": "Main", "bullets": ["Detail 1"], "speaker_notes": ""},
]


def _mock_openai(content: str):
    """Return a patched OpenAI client that yields *content* as the reply."""
    mock_client = MagicMock()
    mock_choice = MagicMock()
    mock_choice.message.content = content
    mock_client.chat.completions.create.return_value = MagicMock(choices=[mock_choice])
    return mock_client


class TestBuildPrompt:
    def test_contains_topic(self):
        prompt = _build_prompt("Machine Learning", 5)
        assert "Machine Learning" in prompt

    def test_contains_slide_count(self):
        prompt = _build_prompt("AI", 7)
        assert "7" in prompt


class TestGenerateOutline:
    @patch("src.slide_generator.OpenAI")
    @patch("src.slide_generator.get_config")
    def test_returns_slides(self, mock_cfg, mock_openai_cls):
        cfg = MagicMock()
        cfg.validate.return_value = []
        cfg.openai_api_key = "test-key"
        cfg.openai_base_url = "https://api.openai.com/v1"
        cfg.openai_model = "gpt-4o"
        cfg.max_slides = 20
        mock_cfg.return_value = cfg
        mock_openai_cls.return_value = _mock_openai(json.dumps(SAMPLE_SLIDES))

        slides = generate_outline("Python", num_slides=2)

        assert len(slides) == 2
        assert isinstance(slides[0], Slide)
        assert slides[0].title == "Intro"
        assert slides[1].bullets == ["Detail 1"]

    @patch("src.slide_generator.get_config")
    def test_raises_on_invalid_config(self, mock_cfg):
        cfg = MagicMock()
        cfg.validate.return_value = ["OPENAI_API_KEY is required but not set."]
        mock_cfg.return_value = cfg

        with pytest.raises(ValueError, match="Invalid configuration"):
            generate_outline("topic")
