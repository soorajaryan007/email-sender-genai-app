import dotenv from "dotenv";
dotenv.config();

export const settings = {
  groqApiKey: process.env.GROQ_API_KEY,
  groqModel: process.env.GROQ_MODEL || "llama-3.3-70b-versatile",
  groqTemperature: Number(process.env.GROQ_TEMPERATURE || 0.4),
  groqMaxTokens: Number(process.env.GROQ_MAX_TOKENS || 1024),
  appEnv: process.env.APP_ENV || "development",
};
