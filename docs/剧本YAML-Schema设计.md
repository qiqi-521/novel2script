# 剧本 YAML Schema 设计文档

## 1. 文档目的

本文档定义 novel2script 的剧本 YAML 输出结构。

当前项目的 YAML 结果后续会继续给 AI 阅读、改写、扩写或局部重生成，因此默认 Schema 不应追求字段完整，而应追求：

1. 字段少，减少 token 成本。
2. 结构稳定，便于 AI 和程序解析。
3. 语义清晰，便于用户阅读和编辑。
4. 保留剧本改写所需的核心信息。

本项目采用一套轻量 Schema：

```text
用户输入小说 -> AI 生成轻量 JSON -> Pydantic 校验 -> 程序转换为 YAML
```

AI 生成的 JSON 和最终导出的 YAML 使用同一组字段，区别只在序列化格式不同。

## 2. 设计原则

### 2.1 AI 优先

YAML 后续主要会被 AI 继续处理，因此字段必须减少冗余解释，避免模型在无关元数据上浪费上下文。

### 2.2 内容优先

默认 YAML 应突出剧本内容本身：角色、场景、动作、对白、旁白。

### 2.3 可编辑

剧本内容仍然需要拆成可编辑的 `beats`，不能只输出整场大段文本。

### 2.4 少 ID

默认 Schema 直接使用角色名，不使用 `char_001`、`scene_001`、`beat_001` 这类机器 ID。

### 2.5 不输出调试字段

追踪、校验、告警、改编说明等字段不进入首版默认 Schema，避免输出越来越重。

## 3. 默认 YAML 结构

默认输出结构如下：

```yaml
title: 雨夜来信
mode: balanced

characters:
  - name: 林晚
    role: protagonist
    desc: 年轻记者，冷静敏锐，正在追查匿名信真相。
  - name: 陈默
    role: key_support
    desc: 神秘男子，掌握匿名信背后的关键信息。

scenes:
  - title: 雨夜来信
    time: 夜
    location: 旧城区街口
    characters: [林晚]
    summary: 林晚收到匿名信，在雨夜等待即将出现的人。
    beats:
      - type: action
        text: 林晚站在旧城区街口，手中攥着被雨水打湿的匿名信。
      - type: narration
        text: 她意识到，这封信会把她带进一场危险的局。

  - title: 巷口脚步
    time: 夜
    location: 旧城区巷口
    characters: [林晚]
    summary: 林晚听见巷子深处传来脚步声，等待的人终于出现。
    beats:
      - type: action
        text: 巷子深处传来缓慢而清晰的脚步声。
      - type: action
        text: 林晚屏住呼吸，盯着黑暗尽头。

  - title: 陈默现身
    time: 夜
    location: 巷口
    characters: [林晚, 陈默]
    summary: 陈默现身，暗示自己知道匿名信的来历。
    beats:
      - type: dialogue
        speaker: 陈默
        text: 我知道你为什么会来。
      - type: dialogue
        speaker: 林晚
        text: 那你也该知道，我不会空手回去。
```

## 4. 顶层字段

### 4.1 `title`

类型：`string`

含义：作品或本次改编内容标题。

是否必填：是。

### 4.2 `mode`

类型：`string`

推荐值：

1. `conservative`
2. `balanced`
3. `dramatic`

含义：改编强度。

是否必填：是。

### 4.3 `characters`

类型：`array<object>`

含义：剧本涉及的主要角色。

是否必填：是。

### 4.4 `scenes`

类型：`array<object>`

含义：按剧本场景组织的正文内容。

是否必填：是。

## 5. 角色字段

默认角色结构：

```yaml
characters:
  - name: 林晚
    role: protagonist
    desc: 年轻记者，冷静敏锐，正在追查匿名信真相。
```

字段说明：

1. `name: string`：角色名，必填。
2. `role: string`：角色功能，必填。
3. `desc: string`：角色简短描述，建议填写。

推荐 `role` 值：

1. `protagonist`：主角。
2. `antagonist`：反派或主要阻力角色。
3. `key_support`：关键配角。
4. `support`：普通配角。
5. `minor`：次要角色。

不默认输出的角色字段：

1. `id`：给 AI 看时直接使用角色名即可。
2. `aliases`：仅在角色消歧或别名归一化功能中需要。
3. `goals`：容易让 AI 生成空泛内容，首版用 `desc` 承载即可。
4. `description`：字段名较长，默认 YAML 使用更短的 `desc`。

## 6. 场景字段

默认场景结构：

```yaml
scenes:
  - title: 雨夜来信
    time: 夜
    location: 旧城区街口
    characters: [林晚]
    summary: 林晚收到匿名信，在雨夜等待即将出现的人。
    beats:
      - type: action
        text: 林晚站在旧城区街口，手中攥着被雨水打湿的匿名信。
```

字段说明：

1. `title: string`：场景标题，必填。
2. `time: string`：场景时间，如 `夜`、`清晨`、`数日后`。
3. `location: string`：场景地点。
4. `characters: array<string>`：本场出场角色名。
5. `summary: string`：场景摘要。
6. `beats: array<object>`：场景内的动作、对白或旁白。

不默认输出的场景字段：

1. `id`：对 AI 后续处理价值低。
2. `chapter_refs`：只有做原文对照时才需要。
3. `characters_present`：字段过长，默认 YAML 改为 `characters`。
4. `scene_purpose`：和 `summary` 重叠，容易产生解释性废话。
5. `adaptation_notes`：占用 token，默认不输出。

## 7. Beats 字段

`beats` 是最小可编辑内容单元。

默认结构：

```yaml
beats:
  - type: action
    text: 林晚停下脚步，低头看了一眼手中的匿名信。
  - type: dialogue
    speaker: 林晚
    text: 如果这封信是真的，今晚一定有人会来。
  - type: narration
    text: 远处传来脚步声，巷子里的气氛骤然紧绷。
```

字段说明：

1. `type: string`：内容类型，必填。
2. `speaker: string`：对白说话人，仅 `type = dialogue` 时填写。
3. `text: string`：动作、对白或旁白正文，必填。

推荐 `type` 值：

1. `action`：可视动作。
2. `dialogue`：角色对白。
3. `narration`：必要旁白或场景说明。
4. `aside`：少量心理旁白或独白。

不默认输出的 beat 字段：

1. `id`：默认 YAML 不需要逐条机器 ID。
2. `content`：字段名较长，默认 YAML 使用更短的 `text`。
3. `source_type`：解释价值高，但 AI 后续处理时不是必要信息。
4. `emotion`：容易让 AI 硬填，可在后续表演增强功能中再加入。
5. `notes`：调试字段，不进入默认输出。

## 8. 生成链路

本项目推荐并实现以下链路：

```text
用户输入小说 -> AI 生成轻量 JSON -> Pydantic 校验 -> 程序转换为 YAML
```

该链路只有一套默认 Schema。AI 输出的 JSON 和最终 YAML 使用同一组核心字段。

这样做的原因：

1. 实现简单，后端不需要维护额外映射层。
2. AI 一开始就按最终 YAML 结构生成内容，减少字段转换误差。
3. 输出天然更适合后续继续交给 AI 处理。

## 9. 默认不输出字段清单

以下字段不建议进入首版默认 Schema：

| 字段 | 处理方式 | 原因 |
| --- | --- | --- |
| `version` | 删除 | 给 AI 看价值低 |
| `meta.source_type` | 删除 | 当前固定为小说，冗余 |
| `meta.source_chapters` | 后续扩展 | 仅原文追溯需要 |
| `meta.language` | 删除 | 默认中文，冗余 |
| `meta.created_at` | 删除 | 给 AI 无意义 |
| `validation` | 删除 | 属于校验结果，不是剧本正文 |
| `characters.id` | 删除 | 默认直接用角色名 |
| `characters.aliases` | 可选扩展 | 首版不做别名消歧时可省略 |
| `characters.goals` | 可选扩展 | 容易生成空泛目标 |
| `scenes.id` | 删除 | 给 AI 看价值低 |
| `scenes.chapter_refs` | 后续扩展 | 仅原文对照需要 |
| `scenes.scene_purpose` | 删除 | 与 `summary` 功能重叠 |
| `scenes.adaptation_notes` | 调试可选 | 占用 token，默认不输出 |
| `beats.id` | 删除 | 给 AI 看价值低 |
| `beats.source_type` | 调试可选 | 解释字段，默认不输出 |
| `beats.emotion` | 可选扩展 | 后续表演增强再加入 |
| `beats.notes` | 删除 | 调试说明，默认不输出 |

## 10. 字段约束规则

### 10.1 顶层约束

1. 必须包含 `title`、`mode`、`characters`、`scenes`。
2. `characters` 至少包含 1 个角色。
3. `scenes` 至少包含 1 个场景。

### 10.2 角色约束

1. `characters[].name` 不应为空。
2. `characters[].name` 建议唯一。
3. `characters[].role` 应使用推荐值。

### 10.3 场景约束

1. `scenes[].title` 不应为空。
2. `scenes[].characters` 中的名字应能在 `characters[].name` 中找到。
3. 每个场景必须包含至少 1 个 `beat`。

### 10.4 Beat 约束

1. `beats[].type` 必须是推荐值之一。
2. `beats[].text` 不应为空。
3. `type = dialogue` 时必须包含 `speaker`。
4. `type != dialogue` 时不应输出 `speaker`。

## 11. 为什么仍然使用 YAML

YAML 仍然适合作为默认输出格式：

1. 比 JSON 更适合人类阅读和复制。
2. 层级清晰，适合表达角色、场景、beats。
3. 对 AI 也足够友好，尤其在字段压缩后 token 成本更低。
4. 方便用户下载后继续编辑。

注意：AI 仍然生成 JSON，后端校验后再转 YAML。这样能避免 AI 直接生成 YAML 时出现缩进错误或结构不稳定。

## 12. 后续扩展字段

以下字段可以后续按功能单独增加，但不进入首版默认 YAML：

1. `relations`：角色关系图谱。
2. `style`：改编风格或语言风格。
3. `scene_metrics`：对白占比、冲突强度、场景长度。
4. `source_refs`：原文追溯信息。
5. `regeneration_context`：局部重生成上下文。
6. `review_notes`：用户或系统审阅意见。

这些扩展应按需开启，避免默认 YAML 越来越重。

## 13. 结论

新的 YAML Schema 采用轻量设计：

```text
title + mode + characters + scenes + beats
```

它不再把追踪字段、解释字段和告警字段输出给用户或 AI。

这样做的好处是：

1. 降低后续 AI 处理的 token 成本。
2. 减少无关字段对 AI 的干扰。
3. 保留剧本改写、预览和局部编辑所需的核心结构。
4. 让 AI 生成 JSON 和最终 YAML 使用同一套简单结构。

因此，代码实现应保持简单：AI 生成轻量 JSON，后端校验后直接转 YAML。
