"""Tests for slide_renderer and exporter modules."""
import pytest
from pathlib import Path
from src.slide_generator import Slide
from src.slide_renderer import render_slide, render_outline, outline_to_markdown
from src.exporter import export, export_markdown, export_html


SAMPLE_SLIDES = [
    Slide(title="Introduction", content=["What is AI?", "Why it matters"]),
    Slide(title="Use Cases", content=["Healthcare", "Finance", "Education"]),
]


class TestRenderSlide:
    def test_index_assigned(self):
        rendered = render_slide(SAMPLE_SLIDES[0], 1)
        assert rendered.index == 1

    def test_title_preserved(self):
        rendered = render_slide(SAMPLE_SLIDES[0], 1)
        assert rendered.title == "Introduction"

    def test_bullets_populated(self):
        rendered = render_slide(SAMPLE_SLIDES[0], 1)
        assert "What is AI?" in rendered.bullets

    def test_empty_bullets_stripped(self):
        slide = Slide(title="Empty", content=["  ", "Valid point", ""])
        rendered = render_slide(slide, 1)
        assert rendered.bullets == ["Valid point"]


class TestRenderOutline:
    def test_length_matches(self):
        rendered = render_outline(SAMPLE_SLIDES)
        assert len(rendered) == len(SAMPLE_SLIDES)

    def test_indices_sequential(self):
        rendered = render_outline(SAMPLE_SLIDES)
        assert [r.index for r in rendered] == [1, 2]


class TestOutlineToMarkdown:
    def test_contains_titles(self):
        md = outline_to_markdown(SAMPLE_SLIDES)
        assert "Introduction" in md
        assert "Use Cases" in md

    def test_contains_bullets(self):
        md = outline_to_markdown(SAMPLE_SLIDES)
        assert "- Healthcare" in md


class TestExporter:
    def test_export_markdown(self, tmp_path):
        out = tmp_path / "slides.md"
        result = export_markdown(SAMPLE_SLIDES, str(out))
        assert result.exists()
        assert "Introduction" in result.read_text()

    def test_export_html(self, tmp_path):
        out = tmp_path / "slides.html"
        result = export_html(SAMPLE_SLIDES, str(out))
        assert result.exists()
        assert "<h2>" in result.read_text()

    def test_export_auto_detect(self, tmp_path):
        out = tmp_path / "slides.md"
        result = export(SAMPLE_SLIDES, str(out))
        assert result.suffix == ".md"

    def test_export_unsupported_format(self, tmp_path):
        with pytest.raises(ValueError, match="Unsupported format"):
            export(SAMPLE_SLIDES, str(tmp_path / "slides.pptx"))
