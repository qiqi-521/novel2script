"""Core schema models for structured script generation."""

from enum import Enum

from pydantic import BaseModel, Field, field_validator


class AdaptationMode(str, Enum):
    """Supported adaptation styles for script generation."""

    CONSERVATIVE = "conservative"
    BALANCED = "balanced"
    DRAMATIC = "dramatic"


class BeatType(str, Enum):
    """Minimal content unit types inside a scene."""

    ACTION = "action"
    DIALOGUE = "dialogue"
    NARRATION = "narration"
    ASIDE = "aside"


class HealthResponse(BaseModel):
    """Health check response model."""

    status: str = "ok"


class GenerateScriptRequest(BaseModel):
    """Request model for the mock script generation endpoint."""

    title: str = Field(..., min_length=1, max_length=200)
    content: str = Field(..., min_length=50)
    adaptation_mode: AdaptationMode = AdaptationMode.BALANCED

    @field_validator("title", "content")
    @classmethod
    def strip_required_text(cls, value: str) -> str:
        cleaned = value.strip()
        if not cleaned:
            raise ValueError("must not be empty")
        return cleaned


class ParseNovelRequest(BaseModel):
    """Request model for novel chapter parsing."""

    content: str = Field(..., min_length=50)

    @field_validator("content")
    @classmethod
    def strip_content(cls, value: str) -> str:
        cleaned = value.strip()
        if not cleaned:
            raise ValueError("must not be empty")
        return cleaned


class ChapterSegment(BaseModel):
    """Structured chapter data extracted from the raw novel input."""

    index: int
    title: str
    content: str
    character_count: int


class ParseNovelResponse(BaseModel):
    """Parsed chapter output returned by the ingestion API."""

    chapter_count: int
    total_characters: int
    chapters: list[ChapterSegment]


class ExtractStoryStructureRequest(BaseModel):
    """Request model for character and event extraction."""

    content: str = Field(..., min_length=50)

    @field_validator("content")
    @classmethod
    def strip_content(cls, value: str) -> str:
        cleaned = value.strip()
        if not cleaned:
            raise ValueError("must not be empty")
        return cleaned


class CharacterCandidate(BaseModel):
    """Candidate character extracted from the novel text."""

    name: str
    mention_count: int
    chapter_refs: list[int]


class ChapterEvent(BaseModel):
    """Event summary extracted from a chapter."""

    chapter_index: int
    chapter_title: str
    summary: str
    keywords: list[str]
    characters: list[str]
    location_hint: str | None = None


class SceneDraft(BaseModel):
    """Scene draft derived from chapter-level events."""

    id: str
    title: str
    chapter_refs: list[int]
    summary: str
    characters: list[str]
    location_hint: str | None = None


class ExtractStoryStructureResponse(BaseModel):
    """Structured intermediate layer used before script generation."""

    chapter_count: int
    characters: list[CharacterCandidate]
    events: list[ChapterEvent]
    scene_drafts: list[SceneDraft]
    extraction_strategy: str = "AI full-script generation"


class Character(BaseModel):
    """Compact character definition in the script output."""

    name: str
    role: str
    desc: str


class Beat(BaseModel):
    """Minimal editable content unit inside a scene."""

    type: BeatType
    text: str
    speaker: str | None = None


class Scene(BaseModel):
    """Compact scene block in the script output."""

    title: str
    time: str
    location: str
    characters: list[str]
    summary: str
    beats: list[Beat]


class ScriptDocument(BaseModel):
    """Compact structured script document returned by the API."""

    title: str
    mode: AdaptationMode
    characters: list[Character]
    scenes: list[Scene]
