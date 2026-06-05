"""Rule-based intermediate extraction for characters and events."""

from __future__ import annotations

import re
from collections import defaultdict

from backend.app.schemas import (
    ChapterEvent,
    CharacterCandidate,
    ExtractStoryStructureResponse,
    SceneDraft,
)
from backend.app.services.chapter_parser import parse_novel_content

CHARACTER_PATTERN = re.compile(r"[\u4e00-\u9fff]{2,3}")
STOPWORDS = {
    "第1章",
    "第2章",
    "第3章",
    "第4章",
    "旧城区",
    "黑暗里",
    "街口",
    "巷子",
    "今晚",
    "匿名信",
}
EVENT_KEYWORDS = ["来到", "出现", "看向", "盯着", "传来", "问", "走出", "发现", "追踪"]


def extract_story_structure(content: str) -> ExtractStoryStructureResponse:
    """Extract reusable intermediate data from parsed chapter segments."""

    parsed = parse_novel_content(content)

    character_hits: dict[str, set[int]] = defaultdict(set)
    character_counts: dict[str, int] = defaultdict(int)
    events: list[ChapterEvent] = []
    scene_drafts: list[SceneDraft] = []

    for chapter in parsed.chapters:
        names = _extract_character_candidates(chapter.content)
        for name in names:
            character_hits[name].add(chapter.index)
            character_counts[name] += chapter.content.count(name)

        keywords = _extract_keywords(chapter.content)
        summary = _build_summary(chapter.content)
        character_names = sorted(names)[:5]

        events.append(
            ChapterEvent(
                chapter_index=chapter.index,
                chapter_title=chapter.title,
                summary=summary,
                keywords=keywords,
                characters=character_names,
            )
        )

        scene_drafts.append(
            SceneDraft(
                id=f"scene_draft_{chapter.index:03d}",
                title=chapter.title,
                chapter_refs=[chapter.index],
                summary=summary,
                characters=character_names,
            )
        )

    characters = sorted(
        (
            CharacterCandidate(
                name=name,
                mention_count=character_counts[name],
                chapter_refs=sorted(chapter_refs),
            )
            for name, chapter_refs in character_hits.items()
        ),
        key=lambda item: (-item.mention_count, item.name),
    )

    return ExtractStoryStructureResponse(
        chapter_count=parsed.chapter_count,
        characters=characters,
        events=events,
        scene_drafts=scene_drafts,
    )


def _extract_character_candidates(content: str) -> set[str]:
    candidates = set()
    for token in CHARACTER_PATTERN.findall(content):
        if token in STOPWORDS:
            continue
        if token.endswith(("地方", "时候", "出来", "知道", "终于")):
            continue
        candidates.add(token)
    return candidates


def _extract_keywords(content: str) -> list[str]:
    found = [keyword for keyword in EVENT_KEYWORDS if keyword in content]
    if found:
        return found
    return [content[:8]] if content else []


def _build_summary(content: str) -> str:
    sentences = re.split(r"[。！？!?]", content)
    for sentence in sentences:
        cleaned = sentence.strip()
        if cleaned:
            return cleaned[:80]
    return content[:80]
