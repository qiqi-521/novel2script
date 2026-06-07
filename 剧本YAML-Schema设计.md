# 剧本 YAML Schema 设计文档

本文档定义 novel2script 生成的剧本 YAML 结构。

该 Schema 的目标很简单：让 AI 生成的剧本结果既方便人阅读和编辑，也方便后续继续交给 AI 或程序处理。

## Schema 示例

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

## 字段说明

### 顶层字段

- `title`：作品或剧本标题。
- `mode`：改编强度，取值为 `conservative`、`balanced` 或 `dramatic`。
- `characters`：角色列表。
- `scenes`：场景列表。

### 角色字段

- `name`：角色名。
- `role`：角色功能，例如主角、反派、关键配角等。
- `desc`：角色简短描述。

### 场景字段

- `title`：场景标题。
- `time`：场景时间。
- `location`：场景地点。
- `characters`：本场出现的角色名。
- `summary`：场景摘要。
- `beats`：场景中的动作、对白或旁白。

### Beats 字段

- `type`：内容类型，可使用 `action`、`dialogue`、`narration`、`aside`。
- `speaker`：说话人，仅对白需要。
- `text`：具体内容。

## 设计原因

该 Schema 采用轻量结构，原因如下：

1. **结构清晰**：通过 `characters` 和 `scenes` 区分角色与剧情内容。
2. **便于编辑**：每个场景拆成多个 `beats`，用户可以局部修改动作、对白或旁白。
3. **字段足够少**：只保留剧本生成和二次编辑需要的核心信息。
4. **适合 AI 继续处理**：字段语义直接，后续交给 AI 改写或扩写时更稳定。
5. **实现简单**：后端只需要校验一套固定结构，再输出结果。

## 结论

默认 Schema 只保留剧本生成和编辑最需要的内容：

```text
title + mode + characters + scenes + beats
```

这样可以在可读性、可编辑性和实现复杂度之间保持平衡。

