export type AdaptationMode = "conservative" | "balanced" | "dramatic";

export type GenerateScriptPayload = {
  title: string;
  content: string;
  adaptation_mode: AdaptationMode;
};
