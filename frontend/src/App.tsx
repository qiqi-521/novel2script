import { FormEvent, useState } from "react";

import { generateScriptYaml } from "./services/scriptApi";
import type { AdaptationMode } from "./types/script";

const sampleContent = `第1章 雨夜来信
林晚站在旧城区的街口，手里攥着一封已经被雨水打湿的匿名信。她知道今晚一定会有人出现，而这封信会把她带进一场更危险的局里。

第2章 巷口脚步
巷子深处传来缓慢而清晰的脚步声，林晚下意识屏住呼吸，目光死死盯着黑暗尽头。她知道，自己等的人终于来了。

第3章 陈默现身
男人说自己叫陈默，他知道这封信的来历，也知道林晚为什么会被卷入这场风波。`;

const modeOptions: Array<{ label: string; value: AdaptationMode }> = [
  { label: "平衡改编", value: "balanced" },
  { label: "保守改编", value: "conservative" },
  { label: "戏剧化改编", value: "dramatic" },
];

function App() {
  const [title, setTitle] = useState("雨夜来信");
  const [content, setContent] = useState(sampleContent);
  const [mode, setMode] = useState<AdaptationMode>("balanced");
  const [yamlResult, setYamlResult] = useState("");
  const [errorMessage, setErrorMessage] = useState("");
  const [actionMessage, setActionMessage] = useState("");
  const [isGenerating, setIsGenerating] = useState(false);

  const yamlLineCount = yamlResult ? yamlResult.split(/\r?\n/).length : 0;
  const yamlCharacterCount = yamlResult.length;

  async function handleSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    setErrorMessage("");
    setActionMessage("");
    setYamlResult("");

    const cleanedTitle = title.trim();
    const cleanedContent = content.trim();

    if (!cleanedTitle || !cleanedContent) {
      setErrorMessage("标题和小说内容不能为空。");
      return;
    }

    setIsGenerating(true);

    try {
      const result = await generateScriptYaml({
        title: cleanedTitle,
        content: cleanedContent,
        adaptation_mode: mode,
      });
      setYamlResult(result);
    } catch (error) {
      setErrorMessage(error instanceof Error ? error.message : "生成失败，请稍后重试。");
    } finally {
      setIsGenerating(false);
    }
  }

  async function handleCopyYaml() {
    if (!yamlResult) {
      return;
    }

    try {
      await navigator.clipboard.writeText(yamlResult);
      setActionMessage("YAML 已复制到剪贴板。");
    } catch {
      setActionMessage("复制失败，请手动选择结果内容复制。");
    }
  }

  function handleDownloadYaml() {
    if (!yamlResult) {
      return;
    }

    const blob = new Blob([yamlResult], { type: "application/yaml;charset=utf-8" });
    const url = URL.createObjectURL(blob);
    const link = document.createElement("a");
    link.href = url;
    link.download = `${buildSafeFileName(title)}.yaml`;
    document.body.appendChild(link);
    link.click();
    link.remove();
    URL.revokeObjectURL(url);
    setActionMessage("YAML 文件已开始下载。");
  }

  return (
    <main className="shell">
      <section className="intro-panel">
        <p className="eyebrow">novel2script</p>
        <h1>把小说片段变成可编辑剧本 YAML</h1>
        <p className="intro">
          输入三章以上小说文本，选择改编强度，前端会调用后端 AI 生成接口并展示 YAML 初稿。
        </p>
      </section>

      <section className="workspace" aria-label="剧本生成工作区">
        <form className="generator-card" onSubmit={handleSubmit}>
          <label className="field">
            <span>作品标题</span>
            <input
              value={title}
              onChange={(event) => setTitle(event.target.value)}
              placeholder="输入小说或章节标题"
            />
          </label>

          <label className="field">
            <span>改编强度</span>
            <select
              value={mode}
              onChange={(event) => setMode(event.target.value as AdaptationMode)}
            >
              {modeOptions.map((option) => (
                <option key={option.value} value={option.value}>
                  {option.label}
                </option>
              ))}
            </select>
          </label>

          <label className="field field-wide">
            <span>小说正文</span>
            <textarea
              value={content}
              onChange={(event) => setContent(event.target.value)}
              placeholder="粘贴三章以上小说文本"
            />
          </label>

          {errorMessage ? <p className="error-message">{errorMessage}</p> : null}

          <button className="primary-action" type="submit" disabled={isGenerating}>
            {isGenerating ? "生成中..." : "生成剧本 YAML"}
          </button>
        </form>

        <article className="result-card">
          <div className="result-header">
            <div>
              <p className="eyebrow">output</p>
              <h2>YAML 结果</h2>
            </div>
            {yamlResult ? <span className="status-pill">已生成</span> : <span className="status-pill muted">等待输入</span>}
          </div>

          <div className="result-toolbar" aria-label="YAML 结果操作">
            <div className="result-stats">
              <span>{yamlLineCount} 行</span>
              <span>{yamlCharacterCount} 字符</span>
            </div>
            <div className="result-actions">
              <button type="button" onClick={handleCopyYaml} disabled={!yamlResult}>
                复制 YAML
              </button>
              <button type="button" onClick={handleDownloadYaml} disabled={!yamlResult}>
                下载 YAML
              </button>
            </div>
          </div>

          {actionMessage ? <p className="action-message">{actionMessage}</p> : null}

          <pre className="yaml-preview">
            {yamlResult || "生成后的剧本 YAML 会显示在这里。"}
          </pre>
        </article>
      </section>
    </main>
  );
}

function buildSafeFileName(rawTitle: string): string {
  const cleaned = rawTitle.trim().replace(/[\\/:*?"<>|\s]+/g, "-");
  return cleaned || "script";
}

export default App;
