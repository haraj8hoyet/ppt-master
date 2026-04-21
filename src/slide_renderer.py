"""Render slide outlines into formatted presentation content."""
from dataclasses import dataclass
from typing import List
from src.slide_generator import Slide


@dataclass
class RenderedSlide:
    index: int
    title: str
    bullets: List[str]
    speaker_notes: str = ""

    def to_markdown(self) -> str:
        lines = [f"## Slide {self.index}: {self.title}"]
        for bullet in self.bullets:
            lines.append(f"- {bullet}")
        if self.speaker_notes:
            # Notes are separated by a blank line for readability
            lines.append(f"\n> Notes: {self.speaker_notes}")
        return "\n".join(lines)


def render_slide(slide: Slide, index: int) -> RenderedSlide:
    """Convert a Slide dataclass into a RenderedSlide."""
    bullets = [point.strip() for point in slide.content if point.strip()]
    return RenderedSlide(
        index=index,
        title=slide.title,
        bullets=bullets,
        # Carry over speaker notes if the Slide object has them
        speaker_notes=getattr(slide, "speaker_notes", ""),
    )


def render_outline(slides: List[Slide]) -> List[RenderedSlide]:
    """Render a full list of slides."""
    return [render_slide(slide, i + 1) for i, slide in enumerate(slides)]


def outline_to_markdown(slides: List[Slide]) -> str:
    """Convert a slide outline to a full markdown document.

    Slides are separated by a horizontal rule so they're easier to distinguish
    when previewing in VS Code or pasting into a doc. Previously used two
    newlines but I found the divider much cleaner for longer decks.
    """
    rendered = render_outline(slides)
    sections = [r.to_markdown() for r in rendered]
    # Use HR separator instead of just double newline for clearer slide boundaries
    return "\n\n---\n\n".join(sections)
