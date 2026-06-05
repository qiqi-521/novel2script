# 剧本 YAML Schema 设计文档

## 1. 文档目的

本文档用于定义 AI 小说转剧本工具的剧本 YAML Schema，明确输出数据的结构、字段含义、约束规则与设计原因。

该 Schema 的目标不是做一份“文学文本存档格式”，而是做一份同时满足以下三类需求的结构化剧本格式：

1. 适合 AI 直接生成结构化 JSON，并由后端进行 Schema 校验。
2. 适合人类作者阅读、修改与继续打磨。
3. 适合后续程序继续消费，例如预览、局部重生成、导出和一致性检查。

当前实现路径为：AI 根据小说原文直接生成符合本 Schema 的 JSON；后端使用 Pydantic 校验 JSON；校验通过后再序列化为 YAML。后端不再通过硬编码规则判断角色、地点、事件或对白。

## 2. 设计目标

本 Schema 设计遵循以下目标：

### 2.1 可读性

YAML 最终会直接展示给用户，因此字段命名应清晰，层级不能过深，结构应尽量贴近用户对“剧本”的理解方式。

### 2.2 可解析性

Schema 需要便于前后端程序解析和校验，避免大量不定形自由文本，尽量将结构拆成稳定字段。

### 2.3 可编辑性

用户后续需要修改单场、单句对白或单个动作，因此内容单元不能全部堆成大段文本，必须拆为可独立编辑的条目。

### 2.4 可扩展性

首版输出的是剧本初稿，但后续可能增加角色卡、分镜、节奏分析、局部重生成等能力，因此 Schema 需要预留扩展空间。

### 2.5 可追踪性

小说改编不是纯生成任务，很多内容来自原文提炼，部分内容来自模型补写，因此 Schema 应能记录必要的来源信息或改编说明。

## 3. 总体结构

顶层建议采用如下结构：

```yaml
version: "1.0"
meta:
  title: "作品名"
  source_type: "novel"
  source_chapters:
    start: 1
    end: 3
  language: "zh-CN"
  adaptation_mode: "balanced"
  created_at: "2026-06-05T14:30:00+08:00"
  summary: "三章内容改编后的剧本简介"
characters:
  - id: "char_linwan"
    name: "林晚"
    aliases: ["晚晚", "林小姐"]
    role_type: "protagonist"
    description: "女主，性格冷静，观察力强"
    goals: ["查明真相"]
scenes:
  - id: "scene_001"
    chapter_refs: [1]
    title: "雨夜初遇"
    time: "夜"
    location: "旧城区巷口"
    characters_present: ["char_linwan", "char_chenmo"]
    scene_purpose: "建立主角相遇与初始冲突"
    summary: "林晚在雨夜追踪线索，与陈默发生第一次正面接触。"
    beats:
      - type: "action"
        content: "林晚撑伞快步穿过巷口，鞋跟在积水中溅起水花。"
        source_type: "adapted"
      - type: "dialogue"
        speaker: "char_chenmo"
        content: "你跟了我一路，到底想知道什么？"
        source_type: "adapted"
      - type: "dialogue"
        speaker: "char_linwan"
        content: "我只想确认，你今晚为什么会出现在这里。"
        source_type: "adapted"
    adaptation_notes:
      compression: "压缩了原文中连续三段环境描写"
      inner_monologue_strategy: "将主角心理紧张感转写为动作与停顿"
validation:
  warnings: []
```

## 4. 顶层字段设计

### 4.1 `version`

含义：

用于标记 Schema 版本。

类型：

`string`

设计原因：

1. 便于未来升级字段结构时做兼容处理。
2. 前后端和导出模块可根据版本选择不同解析策略。

### 4.2 `meta`

含义：

描述本次剧本输出的元信息。

类型：

`object`

推荐字段：

1. `title`：作品标题。
2. `source_type`：来源类型，首版固定为 `novel`。
3. `source_chapters`：原文章节范围。
4. `language`：语言标记。
5. `adaptation_mode`：改编强度或风格模式。
6. `created_at`：生成时间。
7. `summary`：改编结果摘要。

设计原因：

1. 元信息独立存放，便于展示和检索。
2. `adaptation_mode` 是创新功能的重要基础字段。
3. `source_chapters` 直接体现该作品对应哪一段原文。

### 4.3 `characters`

含义：

剧本涉及的角色定义列表。

类型：

`array<object>`

设计原因：

1. 将角色集中定义，避免在每个场景里重复写角色说明。
2. 角色独立成表后，便于做一致性检查和角色关系扩展。

### 4.4 `scenes`

含义：

剧本的核心内容，按场次组织。

类型：

`array<object>`

设计原因：

1. 剧本天然以“场景”为主组织单元，而不是按章节或段落。
2. 以场为单位便于单场编辑、单场重生成和节奏分析。

### 4.5 `validation`

含义：

记录生成后发现的校验结果、提示或告警。

类型：

`object`

设计原因：

1. 将结构校验与内容告警结果显式写入输出，便于调试和人工复核。
2. 便于后续接入角色一致性检查、节奏诊断等功能。

## 5. `meta` 字段设计

建议结构如下：

```yaml
meta:
  title: "迷雾之城"
  source_type: "novel"
  source_chapters:
    start: 1
    end: 3
  language: "zh-CN"
  adaptation_mode: "balanced"
  created_at: "2026-06-05T14:30:00+08:00"
  summary: "围绕匿名信展开的悬疑开篇，完成主角相遇和首轮冲突建立。"
```

字段说明：

1. `title: string`
2. `source_type: string`
3. `source_chapters.start: integer`
4. `source_chapters.end: integer`
5. `language: string`
6. `adaptation_mode: string`
7. `created_at: datetime-string`
8. `summary: string`

设计原因：

1. `source_chapters` 使用对象而不是 `"1-3"` 这种字符串，是为了便于程序处理。
2. `adaptation_mode` 单独存储，便于比较不同模式下生成结果。
3. `summary` 有助于用户快速判断本次输出是否符合预期。

## 6. `characters` 字段设计

建议结构如下：

```yaml
characters:
  - id: "char_linwan"
    name: "林晚"
    aliases: ["晚晚", "林小姐"]
    role_type: "protagonist"
    description: "年轻记者，冷静敏锐，执着追查真相。"
    goals:
      - "查明匿名信背后的秘密"
  - id: "char_chenmo"
    name: "陈默"
    aliases: []
    role_type: "key_support"
    description: "神秘男子，掌握关键信息但刻意隐瞒。"
    goals:
      - "隐藏自己的真实来意"
```

字段说明：

1. `id: string`
2. `name: string`
3. `aliases: array<string>`
4. `role_type: string`
5. `description: string`
6. `goals: array<string>`

设计原因：

1. 使用 `id` 而不是直接用角色名做引用，便于处理重名、别名和改名问题。
2. `aliases` 用于角色归一化，是解决小说中多称谓问题的关键字段。
3. `role_type` 便于后续做主演、配角、功能角色筛选。
4. `goals` 不是必须字段，但它有助于剧本生成时维持角色行为一致性。

推荐的 `role_type` 可选值：

1. `protagonist`
2. `antagonist`
3. `key_support`
4. `support`
5. `minor`
6. `extra`

## 7. `scenes` 字段设计

这是 Schema 的核心部分。

建议结构如下：

```yaml
scenes:
  - id: "scene_001"
    chapter_refs: [1]
    title: "雨夜初遇"
    time: "夜"
    location: "旧城区巷口"
    characters_present: ["char_linwan", "char_chenmo"]
    scene_purpose: "建立主角相遇与试探关系"
    summary: "林晚跟踪线索来到旧城区，与陈默在雨夜相遇并展开第一次交锋。"
    beats:
      - id: "beat_001"
        type: "action"
        content: "林晚撑着黑伞站在巷口，视线始终没有离开前方的人影。"
        source_type: "adapted"
      - id: "beat_002"
        type: "dialogue"
        speaker: "char_chenmo"
        content: "你打算躲到什么时候？"
        source_type: "adapted"
      - id: "beat_003"
        type: "action"
        content: "林晚收起手机，从阴影里走出来，神色警惕。"
        source_type: "adapted"
      - id: "beat_004"
        type: "dialogue"
        speaker: "char_linwan"
        content: "我只是比你先一步发现，有些事不该被埋掉。"
        source_type: "generated"
    adaptation_notes:
      compression: "将原文两页追踪过程压缩为一个开场动作段"
      dialogue_strategy: "保留试探语气，减少解释性台词"
      inner_monologue_strategy: "用动作和神态代替大段心理描写"
```

### 7.1 场景基础字段

字段说明：

1. `id: string`
2. `chapter_refs: array<integer>`
3. `title: string`
4. `time: string`
5. `location: string`
6. `characters_present: array<string>`
7. `scene_purpose: string`
8. `summary: string`
9. `beats: array<object>`
10. `adaptation_notes: object`

设计原因：

1. `chapter_refs` 用于追溯该场景对应哪些原文章节。
2. `title` 方便用户快速定位场景内容。
3. `scene_purpose` 是非常重要的业务字段，它明确该场的戏剧功能，便于压缩和重写时不丢失主目标。
4. `summary` 提供场景级概览，适合列表预览与节奏检查。

### 7.2 为什么不用“整场纯文本”

如果每场只保留一个大文本字段，例如 `script_text`，会带来以下问题：

1. 用户难以只修改一条对白或一个动作。
2. 程序难以检查说话人、动作和旁白结构。
3. 局部重生成会缺少精确定位点。
4. 后续难以扩展为分镜、语音或角色分析模块。

因此，每场必须拆成 `beats` 列表。

## 8. `beats` 内容单元设计

`beats` 是场景内部最核心的可编辑内容单元，表示一个连续的剧本动作点、对白点或说明点。

建议字段如下：

1. `id`
2. `type`
3. `speaker`
4. `content`
5. `source_type`
6. `emotion`
7. `notes`

推荐结构如下：

```yaml
beats:
  - id: "beat_001"
    type: "action"
    content: "林晚停下脚步，低头看了一眼手中的匿名信。"
    source_type: "adapted"
  - id: "beat_002"
    type: "dialogue"
    speaker: "char_linwan"
    content: "如果这封信是真的，今晚一定有人会来。"
    emotion: "压抑、警觉"
    source_type: "generated"
  - id: "beat_003"
    type: "narration"
    content: "远处传来脚步声，巷子里的气氛骤然紧绷。"
    source_type: "adapted"
```

字段说明：

### 8.1 `id`

类型：

`string`

设计原因：

为局部编辑、排序、评论和重生成提供稳定锚点。

### 8.2 `type`

类型：

`string`

推荐值：

1. `action`
2. `dialogue`
3. `narration`
4. `aside`

设计原因：

1. 明确区分动作、对白和说明，便于展示与导出。
2. `aside` 可用于少量必要的心理旁白或导演提示。

### 8.3 `speaker`

类型：

`string | null`

适用条件：

仅当 `type = dialogue` 时必填。

设计原因：

1. 说话人必须显式绑定角色。
2. 可用于角色一致性校验和对白筛选。

### 8.4 `content`

类型：

`string`

设计原因：

1. 作为最核心文本字段，必须保持单条内容语义完整。
2. 不拆成更细 token 级结构，以控制复杂度。

### 8.5 `source_type`

类型：

`string`

推荐值：

1. `quoted`
2. `adapted`
3. `generated`

设计原因：

这是本 Schema 的关键创新字段之一。

1. `quoted` 表示基本来自原文直接引语。
2. `adapted` 表示基于原文内容压缩、改写或转写。
3. `generated` 表示模型为增强戏剧性或连贯性而补写。

该字段的价值在于：

1. 让“AI 改编”过程更可解释。
2. 方便用户重点检查模型补写内容。
3. 为评审展示业务深度提供依据。

### 8.6 `emotion`

类型：

`string`

是否必需：

非必填。

设计原因：

保留少量情绪提示，有利于表演理解，也有利于后续语气重生成，但不应强制要求每条都填。

### 8.7 `notes`

类型：

`string`

是否必需：

非必填。

设计原因：

用于补充个别条目的特殊说明，避免污染主字段结构。

## 9. `adaptation_notes` 设计

建议结构如下：

```yaml
adaptation_notes:
  compression: "删减了大段环境铺陈，保留人物追踪与相遇结果"
  dialogue_strategy: "将叙述中的试探关系改写成两轮短对白"
  inner_monologue_strategy: "通过停顿、视线移动和动作替代心理独白"
  risk_flags:
    - "本场陈默的台词部分为补写，建议人工复核人物口吻"
```

字段说明：

1. `compression`
2. `dialogue_strategy`
3. `inner_monologue_strategy`
4. `risk_flags`

设计原因：

1. 这是对“小说怎么转剧本”的显式记录。
2. 它不是面向最终观众，而是面向作者和开发者，帮助理解改编决策。
3. 评审看到这部分，可以直接理解本项目不是黑盒生成。

## 10. `validation` 设计

建议结构如下：

```yaml
validation:
  warnings:
    - code: "SCENE_CHARACTER_MISMATCH"
      message: "scene_003 中出现 speaker=char_moli，但该角色不在 characters_present 中"
    - code: "EXCESSIVE_GENERATION"
      message: "scene_005 中 generated 类型条目占比过高，建议人工复核"
```

设计原因：

1. 输出不仅有内容，也应有自检结果。
2. 这可以支持角色一致性检查和质量诊断能力。
3. 即使首版告警规则较少，字段先设计出来，后续扩展成本更低。

## 11. 字段约束规则

为保证 Schema 稳定性，建议定义以下约束：

### 11.1 顶层约束

1. 必须包含 `version`、`meta`、`characters`、`scenes`。
2. `scenes` 至少包含 1 个场景。

### 11.2 角色约束

1. `characters[].id` 必须唯一。
2. `characters[].name` 不应为空。

### 11.3 场景约束

1. `scenes[].id` 必须唯一。
2. `characters_present` 中的角色引用必须出现在 `characters[].id` 中。
3. 每个场景必须包含至少 1 个 `beat`。

### 11.4 内容单元约束

1. `beats[].id` 在单场内必须唯一。
2. `beats[].type = dialogue` 时，`speaker` 必填。
3. `beats[].type != dialogue` 时，`speaker` 应为空或省略。
4. `content` 不应为空字符串。

### 11.5 质量约束

1. `generated` 条目占比不应过高，否则需要给出告警。
2. 单个场景不应只有说明文字而没有动作或对白，除非该场被明确标记为过渡场。

## 12. 为什么选择 YAML

本项目要求输出 YAML，这一格式也确实适合当前场景。原因如下：

1. 对人类更友好，便于阅读和手工修改。
2. 能表达层级结构，适合角色、场景、内容单元这类嵌套关系。
3. 与 JSON 相比噪音更少，更适合作为用户可见输出。
4. 便于后续使用标准解析器做校验、导出与转换。

同时，为降低 YAML 出错率，系统实现中采用：

1. AI 先生成结构化 JSON，而不是直接生成 YAML。
2. 后端使用 Pydantic 将 JSON 校验为 `ScriptDocument`。
3. 校验通过后由程序序列化为 YAML。
4. 校验失败时返回错误，避免输出半结构化或不可解析内容。

## 13. 设计取舍说明

### 13.1 为什么顶层不直接按章节组织

因为小说的章节边界不等于剧本的场次边界。一个章节可能拆成多个场景，多个章节也可能合并成一条连续戏剧线。因此顶层必须以 `scenes` 为核心。

### 13.2 为什么保留 `chapter_refs`

虽然顶层不按章节组织，但改编追溯仍然重要。`chapter_refs` 能帮助用户理解某场内容来自哪些章节，也方便后续做原文对照。

### 13.3 为什么要区分 `quoted`、`adapted`、`generated`

这是为了把“提炼原文”和“模型补写”区分开。否则用户无法判断哪些内容更接近原著，哪些内容需要重点复核。

### 13.4 为什么不把角色关系直接塞进场景里

角色关系是跨场景稳定存在的全局信息，放在 `characters` 层或未来独立 `relations` 层更合理。场景只保留当前出场角色即可。

### 13.5 为什么 `adaptation_notes` 不是必填

首版系统的重点还是稳定生成剧本主体。如果强制每场都生成完整说明，可能拉高模型负担并降低稳定性。因此建议保留该字段，但允许按需输出。

## 14. 首版推荐最小可用 Schema

如果首版开发时间紧，建议至少保证以下字段：

```yaml
version: "1.0"
meta:
  title: "作品名"
  source_chapters:
    start: 1
    end: 3
  adaptation_mode: "balanced"
characters:
  - id: "char_001"
    name: "主角"
scenes:
  - id: "scene_001"
    chapter_refs: [1]
    title: "场景标题"
    location: "地点"
    characters_present: ["char_001"]
    beats:
      - id: "beat_001"
        type: "dialogue"
        speaker: "char_001"
        content: "对白内容"
        source_type: "adapted"
```

原因：

1. 这套最小结构已经能支撑“输入-生成-导出-预览”的基本闭环。
2. 其他字段可以逐步补齐，不影响总体方向。

## 15. 后续扩展方向

后续可在不破坏主结构的情况下扩展以下内容：

1. `relations`：角色关系图谱。
2. `style_profile`：改编风格配置。
3. `scene_metrics`：场景长度、对白占比、冲突强度等指标。
4. `regeneration_context`：局部重生成上下文。
5. `storyline_tags`：主线、副线、情感线等标签。

## 16. 结论

本 Schema 的核心设计思想是：以 `场景` 作为主组织单元，以 `beats` 作为最小可编辑内容单元，以 `source_type` 和 `adaptation_notes` 体现改编过程的可解释性。

这样设计的好处是：

1. 能贴合小说改编为剧本的真实业务过程。
2. 能支持 AI 生成、规则校验、用户编辑和后续扩展。
3. 能在比赛评审中体现项目对“结构化输出”和“改编逻辑”的理解深度。

因此，这份 Schema 不只是输出格式定义，也是 AI 输出约束、后端校验和 YAML 序列化的共同契约。
