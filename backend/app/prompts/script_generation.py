"""Prompt builder for full-script AI JSON generation."""

from backend.app.schemas import AdaptationMode


def build_script_generation_prompt(title: str, content: str, mode: AdaptationMode) -> str:
    return f"""
你是小说改编剧本工具的核心 AI。请把用户输入的小说内容直接改编成结构化剧本 JSON。

硬性要求：
- 只输出 JSON，不要 Markdown，不要解释。
- 输出必须符合指定轻量结构，后端会直接校验并转成 YAML。
- characters 必须只包含真实人物，不要包含地点、物品、动作、代词或短语碎片。
- scenes 必须根据剧情内容生成，不要使用固定模板。
- 每个 scene 必须包含动作 action、对白 dialogue 或旁白 narration 类型的 beats。
- dialogue 的 speaker 必须使用 characters 中存在的角色 name。
- 尽量抽取真实地点和时间；无法判断时使用“未注明”。
- beat.type 只能是 action、dialogue、narration、aside。
- 改编模式为 {mode.value}：conservative 保守，balanced 平衡，dramatic 戏剧强化。
- 不要输出 version、meta、id、aliases、goals、source_type、validation、adaptation_notes 等冗余字段。

JSON 结构：
{{
  "title": "{title}",
  "mode": "{mode.value}",
  "characters": [
    {{"name": "角色名", "role": "protagonist", "desc": "角色简短说明"}}
  ],
  "scenes": [
    {{
      "title": "场景标题",
      "time": "时间",
      "location": "地点",
      "characters": ["角色名"],
      "summary": "场景摘要",
      "beats": [
        {{"type": "action", "text": "动作描写"}},
        {{"type": "dialogue", "speaker": "角色名", "text": "对白"}}
      ]
    }}
  ]
}}

小说标题：{title}
小说内容：
{content}
""".strip()
