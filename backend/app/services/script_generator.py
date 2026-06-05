"""AI-first script generation service."""

from __future__ import annotations

import json

from fastapi import HTTPException, status
from pydantic import ValidationError

from backend.app.prompts.script_generation import build_script_generation_prompt
from backend.app.schemas import GenerateScriptRequest, ScriptDocument
from backend.app.services.llm_client import LLMClient


def build_script(payload: GenerateScriptRequest) -> ScriptDocument:
    """Generate a complete script JSON with AI and validate it against Schema."""

    prompt = build_script_generation_prompt(
        title=payload.title,
        content=payload.content,
        mode=payload.adaptation_mode,
    )
    raw_content = LLMClient().complete_json(prompt)
    if not raw_content:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="AI 生成不可用，请检查模型配置或稍后重试。",
        )

    try:
        document = ScriptDocument.model_validate(json.loads(raw_content))
    except (json.JSONDecodeError, ValidationError) as exc:
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail=f"AI 返回内容不符合剧本 JSON Schema：{exc}",
        ) from exc

    return document
