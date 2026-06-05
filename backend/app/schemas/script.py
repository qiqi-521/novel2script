"""Core schema models for structured script generation."""

from datetime import datetime, timezone
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


class SceneDraft(BaseModel):
    """Scene draft derived from chapter-level events."""

    id: str
    title: str
    chapter_refs: list[int]
    summary: str
    characters: list[str]


class ExtractStoryStructureResponse(BaseModel):
    """Structured intermediate layer used before script generation."""

    chapter_count: int
    characters: list[CharacterCandidate]
    events: list[ChapterEvent]
    scene_drafts: list[SceneDraft]


class Meta(BaseModel):
    """Top-level metadata for a script document."""

    title: str
    source_type: str = "novel"
    source_chapters: dict[str, int]
    language: str = "zh-CN"
    adaptation_mode: AdaptationMode
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    summary: str


class Character(BaseModel):
    """Character definition in the script output."""

    id: str
    name: str
    aliases: list[str] = Field(default_factory=list)
    role_type: str
    description: str
    goals: list[str] = Field(default_factory=list)


class Beat(BaseModel):
    """Minimal editable content unit inside a scene."""

    id: str
    type: BeatType
    content: str
    source_type: str
    speaker: str | None = None
    emotion: str | None = None


class Scene(BaseModel):
    """Scene block in the script output."""

    id: str
    chapter_refs: list[int]
    title: str
    time: str
    location: str
    characters_present: list[str]
    scene_purpose: str
    summary: str
    beats: list[Beat]
    adaptation_notes: dict[str, str | list[str]] = Field(default_factory=dict)


class ValidationIssue(BaseModel):
    """Non-fatal validation message attached to the generated result."""

    code: str
    message: str


class ValidationResult(BaseModel):
    """Container for warnings produced during generation."""

    warnings: list[ValidationIssue] = Field(default_factory=list)


class ScriptDocument(BaseModel):
    """Structured script document returned by the API."""

    version: str = "1.0"
    meta: Meta
    characters: list[Character]
    scenes: list[Scene]
    validation: ValidationResult = Field(default_factory=ValidationResult)
