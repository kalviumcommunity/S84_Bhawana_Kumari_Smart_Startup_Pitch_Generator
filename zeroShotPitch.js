import OpenAI from "openai";
import dotenv from "dotenv";

dotenv.config();

const client = new OpenAI({
  apiKey: process.env.OPENAI_API_KEY, 
  baseURL: "https://openrouter.ai/api/v1"
});

async function generatePitch(startupIdea) {
  const prompt = `
  You are a professional startup advisor.
  Create a detailed startup pitch for the following idea:
  "${startupIdea}"

  Include:
  1. Problem Statement
  2. Target Audience
  3. Unique Value Proposition
  4. Business Model
  5. Marketing Strategy
  6. Financial Projection
  7. Conclusion
  `;

  const response = await client.chat.completions.create({
    model: "openai/gpt-4o-mini", // OpenRouter model name
    messages: [{ role: "user", content: prompt }],
    temperature: 0.7
  });

  console.log(response.choices[0].message.content);
}

generatePitch("An AI tutor for students");
