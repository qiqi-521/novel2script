import type { GenerateScriptPayload } from "../types/script";

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL ?? "/api";

export async function generateScriptYaml(
  payload: GenerateScriptPayload,
): Promise<string> {
  const response = await fetch(`${API_BASE_URL}/scripts/generate/yaml`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(payload),
  });

  const responseText = await response.text();

  if (!response.ok) {
    throw new Error(parseErrorMessage(responseText, response.status));
  }

  return responseText;
}

function parseErrorMessage(responseText: string, statusCode: number): string {
  if (!responseText) {
    return `生成失败，后端返回状态码 ${statusCode}`;
  }

  try {
    const parsed = JSON.parse(responseText) as { detail?: unknown };
    if (typeof parsed.detail === "string") {
      return parsed.detail;
    }
  } catch {
    return responseText;
  }

  return responseText;
}
