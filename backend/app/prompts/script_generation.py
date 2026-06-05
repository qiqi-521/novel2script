"""Prompt builder for full-script AI JSON generation."""

from backend.app.schemas import AdaptationMode


def build_script_generation_prompt(title: str, content: str, mode: AdaptationMode) -> str:
    return f"""
你是小说改编剧本工具的核心 AI。请把用户输入的小说内容直接改编成结构化剧本 JSON。

硬性要求：
- 只输出 JSON，不要 Markdown，不要解释。
- 输出必须符合指定结构，后端会直接校验并转成 YAML。
- characters 必须只包含真实人物，不要包含地点、物品、动作、代词或短语碎片。
- scenes 必须根据剧情内容生成，不要使用固定模板。
- 每个 scene 必须包含动作 action、对白 dialogue 或旁白 narration 类型的 beats。
- dialogue 的 speaker 必须引用 characters 中存在的角色 id。
- 尽量抽取真实地点和时间；无法判断时使用“未注明”。
- source_type 只能是 quoted、adapted、generated。
- beat.type 只能是 action、dialogue、narration、aside。
- 改编模式为 {mode.value}：conservative 保守，balanced 平衡，dramatic 戏剧强化。

JSON 结构：
{{
  "version": "1.0",
  "meta": {{
    "title": "{title}",
    "source_type": "novel",
    "source_chapters": {{"start": 1, "end": 3}},
    "language": "zh-CN",
    "adaptation_mode": "{mode.value}",
    "summary": "整体改编摘要"
  }},
  "characters": [
    {{"id": "char_001", "name": "角色名", "aliases": [], "role_type": "protagonist", "description": "角色说明", "goals": ["目标"]}}
  ],
  "scenes": [
    {{
      "id": "scene_001",
      "chapter_refs": [1],
      "title": "场景标题",
      "time": "时间",
      "location": "地点",
      "characters_present": ["char_001"],
      "scene_purpose": "本场戏剧功能",
      "summary": "场景摘要",
      "beats": [
        {{"id": "beat_001_001", "type": "action", "content": "动作描写", "source_type": "adapted"}},
        {{"id": "beat_001_002", "type": "dialogue", "speaker": "char_001", "content": "对白", "source_type": "generated", "emotion": "情绪"}}
      ],
      "adaptation_notes": {{"generation_strategy": "AI full-script generation"}}
    }}
  ],
  "validation": {{"warnings": []}}
}}

小说标题：{title}
小说内容：
{content}
""".strip()
