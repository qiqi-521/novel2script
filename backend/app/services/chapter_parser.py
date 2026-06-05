"""Novel chapter parsing and validation service."""

from __future__ import annotations

import re

from fastapi import HTTPException, status

from backend.app.schemas import ChapterSegment, ParseNovelResponse

CHAPTER_HEADER_PATTERN = re.compile(
    r"(?im)^(?P<title>\s*(?:第\s*[0-9零一二三四五六七八九十百千两]+\s*章|chapter\s+\d+)[^\n\r]*)\s*$"
)

MIN_CHAPTERS = 3
MIN_CHARS_PER_CHAPTER = 20


def parse_novel_content(content: str) -> ParseNovelResponse:
    """Split a novel text into chapters and enforce basic validation rules."""

    cleaned = content.strip()
    if not cleaned:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="输入文本不能为空。",
        )

    matches = list(CHAPTER_HEADER_PATTERN.finditer(cleaned))
    if len(matches) < MIN_CHAPTERS:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="输入文本至少需要识别出 3 个章节标题。",
        )

    chapters: list[ChapterSegment] = []
    for index, match in enumerate(matches, start=1):
        start = match.end()
        end = matches[index].start() if index < len(matches) else len(cleaned)
        chapter_content = cleaned[start:end].strip()
        if len(chapter_content) < MIN_CHARS_PER_CHAPTER:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail=f"第 {index} 章正文过短，无法作为有效输入。",
            )

        chapters.append(
            ChapterSegment(
                index=index,
                title=match.group("title").strip(),
                content=chapter_content,
                character_count=len(chapter_content),
            )
        )

    return ParseNovelResponse(
        chapter_count=len(chapters),
        total_characters=sum(chapter.character_count for chapter in chapters),
        chapters=chapters,
    )
