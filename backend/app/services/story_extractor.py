"""AI-first story structure extraction service."""

from __future__ import annotations

import json

from fastapi import HTTPException, status
from pydantic import ValidationError

from backend.app.prompts.script_generation import build_script_generation_prompt
from backend.app.schemas import AdaptationMode, ExtractStoryStructureResponse, ScriptDocument
from backend.app.services.llm_client import LLMClient


def extract_story_structure(content: str) -> ExtractStoryStructureResponse:
    """Generate compact AI script JSON and expose compatible structure fields."""

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
        chapter_count=len(document.scenes),
        characters=[
            {
                "name": character.name,
                "mention_count": 0,
                "chapter_refs": sorted(
                    {
                        index
                        for index, scene in enumerate(document.scenes, start=1)
                        if character.name in scene.characters
                    }
                ),
            }
            for character in document.characters
        ],
        events=[
            {
                "chapter_index": index,
                "chapter_title": scene.title,
                "summary": scene.summary,
                "keywords": [],
                "characters": scene.characters,
                "location_hint": scene.location,
            }
            for index, scene in enumerate(document.scenes, start=1)
        ],
        scene_drafts=[
            {
                "id": f"scene_{index:03d}",
                "title": scene.title,
                "chapter_refs": [index],
                "summary": scene.summary,
                "characters": scene.characters,
                "location_hint": scene.location,
            }
            for index, scene in enumerate(document.scenes, start=1)
        ],
        extraction_strategy="AI compact-script generation",
    )
