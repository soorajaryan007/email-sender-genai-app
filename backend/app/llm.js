import Groq from "groq-sdk";
import { settings } from "./config.js";

const client = new Groq({
  apiKey: settings.groqApiKey,
});

export async function generateColdEmail(prompt, model) {
  const systemPrompt = `
You are a professional email writer.
Do not include subject line.
Write a concise, engaging cold email under 150 words.
Include Candidate Name.
`;

  try {
    const response = await client.chat.completions.create({
      model: model || settings.groqModel,
      messages: [
        { role: "system", content: systemPrompt },
        { role: "user", content: prompt },
      ],
      temperature: settings.groqTemperature,
      max_tokens: settings.groqMaxTokens,
    });

    return response.choices[0].message.content;
  } catch (err) {
    throw new Error(`Groq generation failed: ${err.message}`);
  }
}
