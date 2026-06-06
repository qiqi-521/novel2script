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
  const [isContentFullscreen, setIsContentFullscreen] = useState(false);
  const [isYamlFullscreen, setIsYamlFullscreen] = useState(false);
  const [theme, setTheme] = useState<"light" | "dark">("light");

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
    <main className={`shell shell-${theme}`}>
      <section className="intro-panel">
        <div className="top-nav">
          <p className="eyebrow">novel2script</p>
          <div className="nav-actions">
            <button
              className="theme-toggle"
              type="button"
              onClick={() => setTheme(theme === "light" ? "dark" : "light")}
              aria-label={theme === "light" ? "切换到深色模式" : "切换到浅色模式"}
              title={theme === "light" ? "切换到深色模式" : "切换到浅色模式"}
            >
              {theme === "light" ? (
                <svg aria-hidden="true" viewBox="0 0 16 16">
                  <path d="M9.6 14.7A6.72 6.72 0 0 1 8 1.42a.75.75 0 0 1 .72 1.14 5.22 5.22 0 0 0 4.72 7.72.75.75 0 0 1 1.14.72 6.72 6.72 0 0 1-4.98 3.7Z" />
                </svg>
              ) : (
                <svg aria-hidden="true" viewBox="0 0 16 16">
                  <path d="M8 11.25A3.25 3.25 0 1 0 8 4.75a3.25 3.25 0 0 0 0 6.5Zm0 1.5A4.75 4.75 0 1 1 8 3.25a4.75 4.75 0 0 1 0 9.5ZM8 .25a.75.75 0 0 1 .75.75v.75a.75.75 0 0 1-1.5 0V1A.75.75 0 0 1 8 .25Zm0 13.25a.75.75 0 0 1 .75.75V15a.75.75 0 0 1-1.5 0v-.75A.75.75 0 0 1 8 13.5ZM1 7.25h.75a.75.75 0 0 1 0 1.5H1a.75.75 0 0 1 0-1.5Zm13.25 0H15a.75.75 0 0 1 0 1.5h-.75a.75.75 0 0 1 0-1.5ZM3.05 2.99a.75.75 0 0 1 1.06 0l.53.53a.75.75 0 0 1-1.06 1.06l-.53-.53a.75.75 0 0 1 0-1.06Zm8.31 8.31a.75.75 0 0 1 1.06 0l.53.53a.75.75 0 1 1-1.06 1.06l-.53-.53a.75.75 0 0 1 0-1.06Zm1.59-8.31a.75.75 0 0 1 0 1.06l-.53.53a.75.75 0 0 1-1.06-1.06l.53-.53a.75.75 0 0 1 1.06 0ZM4.64 11.3a.75.75 0 0 1 0 1.06l-.53.53a.75.75 0 0 1-1.06-1.06l.53-.53a.75.75 0 0 1 1.06 0Z" />
                </svg>
              )}
            </button>
            <a
              className="github-link"
              href="https://github.com/qiqi-521/novel2script"
              target="_blank"
              rel="noreferrer"
            >
              <svg aria-hidden="true" viewBox="0 0 16 16">
                <path d="M8 0C3.58 0 0 3.58 0 8c0 3.54 2.29 6.53 5.47 7.59.4.07.55-.17.55-.38 0-.19-.01-.82-.01-1.49-2.01.37-2.53-.49-2.69-.94-.09-.23-.48-.94-.82-1.13-.28-.15-.68-.52-.01-.53.63-.01 1.08.58 1.23.82.72 1.21 1.87.87 2.33.66.07-.52.28-.87.51-1.07-1.78-.2-3.64-.89-3.64-3.95 0-.87.31-1.59.82-2.15-.08-.2-.36-1.02.08-2.12 0 0 .67-.21 2.2.82A7.62 7.62 0 0 1 8 3.86c.68 0 1.36.09 2 .27 1.53-1.04 2.2-.82 2.2-.82.44 1.1.16 1.92.08 2.12.51.56.82 1.27.82 2.15 0 3.07-1.87 3.75-3.65 3.95.29.25.54.73.54 1.48 0 1.07-.01 1.93-.01 2.2 0 .21.15.46.55.38A8.01 8.01 0 0 0 16 8c0-4.42-3.58-8-8-8Z" />
              </svg>
              <span>GitHub</span>
            </a>
          </div>
        </div>
        <div className="hero-copy">
          <span className="hero-badge">AI Script Generator</span>
          <div className="hero-title-row">
            <h1>AI小说转剧本YAML工具</h1>
            <span className="hero-author">作者：刘佳琦</span>
          </div>
        </div>
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
            <div className="novel-editor">
              <textarea
                value={content}
                onChange={(event) => setContent(event.target.value)}
                placeholder="粘贴三章以上小说文本"
              />
              <button
                className="fullscreen-toggle"
                type="button"
                onClick={() => setIsContentFullscreen(true)}
              >
                全屏查看
              </button>
            </div>
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

          <div className="yaml-editor">
            <textarea
              className="yaml-preview"
              value={yamlResult}
              onChange={(event) => setYamlResult(event.target.value)}
              placeholder="生成后的剧本 YAML 会显示在这里。"
              disabled={!yamlResult}
            />
            <button
              className="fullscreen-toggle yaml-fullscreen-toggle"
              type="button"
              onClick={() => setIsYamlFullscreen(true)}
              disabled={!yamlResult}
            >
              全屏查看
            </button>
          </div>
        </article>
      </section>

      {isContentFullscreen ? (
        <div className="fullscreen-editor" role="dialog" aria-modal="true" aria-label="全屏编辑小说正文">
          <div className="fullscreen-editor-card">
            <div className="fullscreen-editor-header">
              <div>
                <p className="eyebrow">novel content</p>
                <h2>小说正文</h2>
              </div>
              <button type="button" onClick={() => setIsContentFullscreen(false)}>
                退出全屏
              </button>
            </div>
            <textarea
              value={content}
              onChange={(event) => setContent(event.target.value)}
              placeholder="粘贴三章以上小说文本"
              autoFocus
            />
          </div>
        </div>
      ) : null}

      {isYamlFullscreen ? (
        <div className="fullscreen-editor yaml-fullscreen-editor" role="dialog" aria-modal="true" aria-label="全屏编辑 YAML 结果">
          <div className="fullscreen-editor-card">
            <div className="fullscreen-editor-header">
              <div>
                <p className="eyebrow">output yaml</p>
                <h2>YAML 结果</h2>
              </div>
              <button type="button" onClick={() => setIsYamlFullscreen(false)}>
                退出全屏
              </button>
            </div>
            <textarea
              className="yaml-preview fullscreen-yaml-preview"
              value={yamlResult}
              onChange={(event) => setYamlResult(event.target.value)}
              placeholder="生成后的剧本 YAML 会显示在这里。"
              autoFocus
            />
          </div>
        </div>
      ) : null}
    </main>
  );
}

function buildSafeFileName(rawTitle: string): string {
  const cleaned = rawTitle.trim().replace(/[\\/:*?"<>|\s]+/g, "-");
  return cleaned || "script";
}

export default App;
