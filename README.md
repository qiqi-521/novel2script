# novel2script

> Demo 视频链接：https://www.bilibili.com/video/BV185Et6GEyE/?vd_source=633c5ce4c5ec091fb5c2de27f15e1104

novel2script 是一个 AI 小说转剧本 YAML 工具。

用户可以输入小说片段，选择改编强度，系统会调用大模型生成结构化剧本，并以 YAML 形式展示。生成后的 YAML 支持在线编辑、复制、下载和全屏查看。

## 核心流程

```text
用户输入小说正文
-> 选择改编强度
-> 后端构造提示词并调用大模型
-> 大模型生成结构化剧本 JSON
-> 后端使用 Pydantic 校验结构
-> 转换为 YAML 返回前端
-> 用户查看、编辑、复制或下载 YAML
```

## 主要功能

- 输入小说正文并生成剧本 YAML
- 支持三种改编强度：保守改编、平衡改编、戏剧化改编
- 自动生成角色、场景、动作、对白和旁白结构
- 支持 YAML 在线编辑、复制和下载
- 支持小说正文和 YAML 结果全屏编辑
- 支持 YAML 行数、字符数、角色数和场景数统计
- 支持浅色 / 深色主题切换

## 技术栈

### 后端

- Python
- FastAPI
- Pydantic
- OpenAI-compatible API
- PyYAML

### 前端

- React
- TypeScript
- Vite

## 环境配置

复制环境变量示例文件：

```powershell
copy .env.example .env
```

然后在 `.env` 中填写大模型配置：

```env
OPENAI_API_KEY=your_api_key_here
OPENAI_BASE_URL=your_openai_compatible_base_url_here
OPENAI_MODEL=your_model_name_here
OPENAI_TIMEOUT_SECONDS=30
```

## 启动后端

在项目根目录执行：

```powershell
uv sync
uv run uvicorn backend.app.main:app --reload
```

后端默认运行在：

```text
http://127.0.0.1:8000
```

## 启动前端

进入前端目录：

```powershell
cd frontend
npm install
npm run dev
```

前端默认运行在：

```text
http://localhost:5173
```

## YAML Schema

剧本 YAML 的结构说明见：

```text
剧本YAML-Schema设计.md
```

## 可改进的点

由于 6 月 8 号毕业答辩，这三天只用了不到一半时间用来做项目，但仍有一些可以改进并且能实现的功能：

1. 在系统提示词的基础上，支持用户自己设计提示词给 AI。
2. 不采用极简风格，增添更细致的 YAML Schema 字段；在必选 YAML 字段的基础上，让用户自己选择是否增添 YAML 字段。
3. 支持各种文件导入并转化为文本。
4. 输入文本过长时提示用户减少输入量。

