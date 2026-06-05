"""Dynamic script generation based on parsed chapters and extracted structure."""

from __future__ import annotations

from backend.app.schemas import (
    AdaptationMode,
    Beat,
    BeatType,
    Character,
    GenerateScriptRequest,
    Meta,
    Scene,
    ScriptDocument,
)
from backend.app.services.story_extractor import extract_story_structure

SUMMARY_BY_MODE = {
    AdaptationMode.CONSERVATIVE: "基于原文章节顺序生成一版偏忠实的结构化剧本初稿。",
    AdaptationMode.BALANCED: "基于章节事件与角色候选生成一版平衡型结构化剧本初稿。",
    AdaptationMode.DRAMATIC: "基于章节事件强化冲突与对白张力，生成一版戏剧化剧本初稿。",
}

SCENE_PURPOSE_BY_MODE = {
    AdaptationMode.CONSERVATIVE: "保持原章核心信息，建立场景基础推进。",
    AdaptationMode.BALANCED: "提炼章节冲突与人物目标，形成清晰场景推进。",
    AdaptationMode.DRAMATIC: "强化章节对抗关系和情绪张力，突出戏剧冲突。",
}

DIALOGUE_BY_MODE = {
    AdaptationMode.CONSERVATIVE: "先把事情说清楚，再决定下一步怎么做。",
    AdaptationMode.BALANCED: "我们已经走到这里了，线索不会自己开口。",
    AdaptationMode.DRAMATIC: "你既然来了，就说明你已经知道这件事没法回头。",
}


def build_script(payload: GenerateScriptRequest) -> ScriptDocument:
    """Build a structured script document from the extracted intermediate layer."""

    extracted = extract_story_structure(payload.content)
    characters = _build_characters(extracted.characters)
    scenes = _build_scenes(extracted.scene_drafts, extracted.events, characters, payload.adaptation_mode)

    chapter_end = extracted.events[-1].chapter_index if extracted.events else 1

    return ScriptDocument(
        meta=Meta(
            title=payload.title,
            source_chapters={"start": 1, "end": chapter_end},
            adaptation_mode=payload.adaptation_mode,
            summary=SUMMARY_BY_MODE[payload.adaptation_mode],
        ),
        characters=characters,
        scenes=scenes,
    )


def _build_characters(character_candidates: list) -> list[Character]:
    if not character_candidates:
        return [
            Character(
                id="char_protagonist",
                name="主角",
                aliases=[],
                role_type="protagonist",
                description="输入文本中未识别到稳定角色名时使用的默认主角。",
                goals=["推动当前章节事件发展"],
            )
        ]

    characters: list[Character] = []
    for index, candidate in enumerate(character_candidates[:5], start=1):
        role_type = "protagonist" if index == 1 else "support"
        characters.append(
            Character(
                id=f"char_{index:03d}",
                name=candidate.name,
                aliases=[],
                role_type=role_type,
                description=f"在输入文本中出现 {candidate.mention_count} 次，涉及章节 {candidate.chapter_refs}。",
                goals=["参与当前章节冲突推进"],
            )
        )
    return characters


def _build_scenes(scene_drafts: list, events: list, characters: list[Character], mode: AdaptationMode) -> list[Scene]:
    character_map = {character.name: character.id for character in characters}
    fallback_speaker = characters[0].id if characters else None
    scenes: list[Scene] = []

    for index, draft in enumerate(scene_drafts, start=1):
        event = events[index - 1] if index - 1 < len(events) else None
        present_ids = [
            character_map[name]
            for name in draft.characters
            if name in character_map
        ]
        if not present_ids and fallback_speaker:
            present_ids = [fallback_speaker]

        beats = [
            Beat(
                id=f"beat_{index:03d}_001",
                type=BeatType.ACTION,
                content=f"{draft.summary}。",
                source_type="adapted",
            ),
            Beat(
                id=f"beat_{index:03d}_002",
                type=BeatType.NARRATION,
                content=_build_narration(event.summary if event else draft.summary, mode),
                source_type="adapted",
            ),
            Beat(
                id=f"beat_{index:03d}_003",
                type=BeatType.DIALOGUE,
                speaker=present_ids[0] if present_ids else fallback_speaker,
                content=DIALOGUE_BY_MODE[mode],
                source_type="generated",
                emotion=_dialogue_emotion(mode),
            ),
        ]

        scenes.append(
            Scene(
                id=f"scene_{index:03d}",
                chapter_refs=draft.chapter_refs,
                title=draft.title,
                time="未注明",
                location="未注明",
                characters_present=present_ids,
                scene_purpose=SCENE_PURPOSE_BY_MODE[mode],
                summary=draft.summary,
                beats=beats,
                adaptation_notes={
                    "compression": "将章节事件压缩为单场景草案。",
                    "dialogue_strategy": f"按 {mode.value} 模式生成基础对白。",
                    "keywords": event.keywords if event else [],
                },
            )
        )

    return scenes


def _build_narration(summary: str, mode: AdaptationMode) -> str:
    if mode is AdaptationMode.CONSERVATIVE:
        return f"场景延续原文章节推进，核心事件为：{summary}。"
    if mode is AdaptationMode.DRAMATIC:
        return f"空气里的紧张感迅速抬升，所有行动都指向同一个冲突核心：{summary}。"
    return f"人物关系和情节压力在这一场逐渐收束到核心问题：{summary}。"


def _dialogue_emotion(mode: AdaptationMode) -> str:
    if mode is AdaptationMode.CONSERVATIVE:
        return "克制、谨慎"
    if mode is AdaptationMode.DRAMATIC:
        return "紧绷、对抗"
    return "警觉、试探"
