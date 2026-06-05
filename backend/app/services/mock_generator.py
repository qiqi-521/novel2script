"""Mock script generation service for the initial backend bootstrap."""

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


def build_mock_script(payload: GenerateScriptRequest) -> ScriptDocument:
    """Return a deterministic script document until the real pipeline is implemented."""

    summary_by_mode = {
        AdaptationMode.CONSERVATIVE: "保留原文主要顺序，生成一版结构化剧本骨架。",
        AdaptationMode.BALANCED: "压缩原文叙述并保留关键冲突，生成一版平衡型剧本初稿。",
        AdaptationMode.DRAMATIC: "强化冲突和对白张力，生成一版戏剧化剧本初稿。",
    }

    scene_purpose_by_mode = {
        AdaptationMode.CONSERVATIVE: "建立主角处境，并尽量忠实保留原文开场信息。",
        AdaptationMode.BALANCED: "建立主角目标与初始冲突，形成清晰的开场场景。",
        AdaptationMode.DRAMATIC: "快速抛出冲突与悬念，提升开场戏剧张力。",
    }

    beats = [
        Beat(
            id="beat_001",
            type=BeatType.ACTION,
            content="主角站在街口，反复确认手中的线索，迟疑片刻后继续向前。",
            source_type="adapted",
        ),
        Beat(
            id="beat_002",
            type=BeatType.DIALOGUE,
            speaker="char_protagonist",
            content="如果这件事是真的，今晚一定会有人出现。",
            source_type="generated",
            emotion="警觉、克制",
        ),
        Beat(
            id="beat_003",
            type=BeatType.NARRATION,
            content="夜色渐深，远处传来的脚步声让气氛骤然紧绷。",
            source_type="adapted",
        ),
    ]

    scene = Scene(
        id="scene_001",
        chapter_refs=[1, 2, 3],
        title="开场试探",
        time="夜",
        location="旧城区街口",
        characters_present=["char_protagonist"],
        scene_purpose=scene_purpose_by_mode[payload.adaptation_mode],
        summary="主角根据线索来到旧城区，确认事件正在朝危险方向发展。",
        beats=beats,
        adaptation_notes={
            "compression": "将多段铺垫性叙述压缩为一个开场场景。",
            "dialogue_strategy": "用短对白显式暴露主角当前判断。",
            "inner_monologue_strategy": "以内化动作和环境反应替代大段心理描写。",
        },
    )

    return ScriptDocument(
        meta=Meta(
            title=payload.title,
            source_chapters={"start": 1, "end": 3},
            adaptation_mode=payload.adaptation_mode,
            summary=summary_by_mode[payload.adaptation_mode],
        ),
        characters=[
            Character(
                id="char_protagonist",
                name="主角",
                aliases=[],
                role_type="protagonist",
                description="基于输入小说自动生成的主角占位角色，用于后续接入真实角色抽取逻辑。",
                goals=["查明线索背后的真相"],
            )
        ],
        scenes=[scene],
    )
