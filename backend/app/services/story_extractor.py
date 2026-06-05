"""AI-first story structure extraction service."""

from __future__ import annotations

import json

from fastapi import HTTPException, status
from pydantic import ValidationError

from backend.app.prompts.script_generation import build_script_generation_prompt
from backend.app.schemas import AdaptationMode, ExtractStoryStructureResponse, ScriptDocument
from backend.app.services.llm_client import LLMClient


def extract_story_structure(content: str) -> ExtractStoryStructureResponse:
    """Generate full AI script JSON and expose its intermediate structure fields."""

    prompt = build_script_generation_prompt(
        title="未命名作品",
        content=content,
        mode=AdaptationMode.BALANCED,
    )
    raw_content = LLMClient().complete_json(prompt)
    if not raw_content:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="AI 结构抽取不可用，请检查模型配置或稍后重试。",
        )

    try:
        document = ScriptDocument.model_validate(json.loads(raw_content))
    except (json.JSONDecodeError, ValidationError) as exc:
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail=f"AI 返回内容不符合剧本 JSON Schema：{exc}",
        ) from exc

    return ExtractStoryStructureResponse(
        chapter_count=document.meta.source_chapters.get("end", len(document.scenes)),
        characters=[
            {
                "name": character.name,
                "mention_count": 0,
                "chapter_refs": sorted(
                    {
                        chapter_ref
                        for scene in document.scenes
                        if character.id in scene.characters_present
                        for chapter_ref in scene.chapter_refs
                    }
                ),
            }
            for character in document.characters
        ],
        events=[
            {
                "chapter_index": scene.chapter_refs[0] if scene.chapter_refs else index,
                "chapter_title": scene.title,
                "summary": scene.summary,
                "keywords": [],
                "characters": [
                    character.name
                    for character in document.characters
                    if character.id in scene.characters_present
                ],
                "location_hint": scene.location,
            }
            for index, scene in enumerate(document.scenes, start=1)
        ],
        scene_drafts=[
            {
                "id": scene.id,
                "title": scene.title,
                "chapter_refs": scene.chapter_refs,
                "summary": scene.summary,
                "characters": [
                    character.name
                    for character in document.characters
                    if character.id in scene.characters_present
                ],
                "location_hint": scene.location,
            }
            for scene in document.scenes
        ],
        extraction_strategy="AI full-script generation",
    )
