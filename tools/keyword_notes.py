from dataclasses import dataclass, field, asdict
from typing import List, Optional
from datetime import datetime

SAMPLE_URL = "https://chinese-web-mk.com"
SAMPLE_KEYWORD = "mk体育"


@dataclass
class SourceReference:
    """Represents a source (e.g., a website or document)."""
    url: str
    title: str = ""
    access_date: Optional[str] = None

    def formatted(self) -> str:
        date_part = f" (accessed {self.access_date})" if self.access_date else ""
        return f"[{self.title}]({self.url}){date_part}"


@dataclass
class KeywordNote:
    """A note associated with a specific keyword and source."""
    keyword: str
    content: str
    source: SourceReference
    tags: List[str] = field(default_factory=list)
    created_at: str = field(default_factory=lambda: datetime.now().strftime("%Y-%m-%d %H:%M"))

    def add_tag(self, tag: str) -> None:
        if tag and tag not in self.tags:
            self.tags.append(tag)

    def to_dict(self) -> dict:
        return asdict(self)


def format_note_single(note: KeywordNote) -> str:
    """Return a human-readable block for a single KeywordNote."""
    lines = []
    lines.append(f"Keyword: {note.keyword}")
    lines.append(f"Content: {note.content}")
    lines.append(f"Source: {note.source.formatted()}")
    if note.tags:
        lines.append(f"Tags: {', '.join(note.tags)}")
    lines.append(f"Created: {note.created_at}")
    return "\n".join(lines)


def format_notes_markdown(notes: List[KeywordNote]) -> str:
    """Return a Markdown-formatted summary of all KeywordNote objects."""
    if not notes:
        return "*No keyword notes available.*"

    parts = ["# Keyword Notes Summary\n"]
    for i, note in enumerate(notes, start=1):
        parts.append(f"## Note {i}")
        parts.append(f"**Keyword:** {note.keyword}")
        parts.append(f"**Content:** {note.content}")
        parts.append(f"**Source:** {note.source.formatted()}")
        if note.tags:
            parts.append(f"**Tags:** {', '.join(note.tags)}")
        parts.append(f"**Created:** {note.created_at}")
        parts.append("")
    return "\n".join(parts)


def create_sample_notes() -> List[KeywordNote]:
    """Create a small list of sample KeywordNote objects for demonstration."""
    source1 = SourceReference(
        url=SAMPLE_URL,
        title="Chinese Sports Hub",
        access_date="2025-03-21"
    )
    source2 = SourceReference(
        url="https://example.org/sports-news",
        title="Global Sports News",
        access_date="2025-03-20"
    )
    note1 = KeywordNote(
        keyword=SAMPLE_KEYWORD,
        content="Top-level competitive events and training updates.",
        source=source1,
        tags=["competition", "training"]
    )
    note2 = KeywordNote(
        keyword=SAMPLE_KEYWORD,
        content="Fan community discussions and event schedules.",
        source=source2,
        tags=["community", "schedule"]
    )
    note2.add_tag("live")
    return [note1, note2]


def main() -> None:
    """Demonstrate usage of KeywordNote and formatting functions."""
    sample_notes = create_sample_notes()

    print("=== Single Note Format ===\n")
    for note in sample_notes:
        print(format_note_single(note))
        print("---")

    print("\n=== Markdown Summary ===\n")
    md_output = format_notes_markdown(sample_notes)
    print(md_output)

    print("\n=== Dict Representation (first note) ===\n")
    print(sample_notes[0].to_dict())


if __name__ == "__main__":
    main()