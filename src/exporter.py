"""Export rendered slides to various output formats."""
from pathlib import Path
from typing import List
from src.slide_generator import Slide
from src.slide_renderer import outline_to_markdown, render_outline


def export_markdown(slides: List[Slide], output_path: str) -> Path:
    """Write slide outline as a Markdown file."""
    path = Path(output_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    content = outline_to_markdown(slides)
    path.write_text(content, encoding="utf-8")
    return path


def export_html(slides: List[Slide], output_path: str) -> Path:
    """Write slide outline as a simple HTML file."""
    path = Path(output_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    rendered = render_outline(slides)
    # Added basic styling so the output is easier to read in a browser
    html_parts = ["<html><head><style>body { font-family: sans-serif; max-width: 800px; margin: 40px auto; } section { border-bottom: 1px solid #ccc; padding-bottom: 1em; margin-bottom: 1em; }</style></head><body>"]
    for slide in rendered:
        html_parts.append(f"<section>")
        html_parts.append(f"<h2>Slide {slide.index}: {slide.title}</h2>")
        html_parts.append("<ul>")
        for bullet in slide.bullets:
            html_parts.append(f"  <li>{bullet}</li>")
        html_parts.append("</ul>")
        if slide.speaker_notes:
            html_parts.append(f"<p><em>{slide.speaker_notes}</em></p>")
        html_parts.append("</section>")
    html_parts.append("</body></html>")
    path.write_text("\n".join(html_parts), encoding="utf-8")
    return path


SUPPORTED_FORMATS = {"md": export_markdown, "html": export_html}


def export(slides: List[Slide], output_path: str) -> Path:
    """Auto-detect format from file extension and export."""
    ext = Path(output_path).suffix.lstrip(".")
    if ext not in SUPPORTED_FORMATS:
        raise ValueError(f"Unsupported format: '{ext}'. Choose from {list(SUPPORTED_FORMATS)}.")
    return SUPPORTED_FORMATS[ext](slides, output_path)
