import { NextResponse } from "next/server";

const SYSTEM_PROMPT = `You are MANSI AI, a warm, feminine, friendly and capable AI companion. Speak naturally in Hinglish when the user uses Hinglish, otherwise match their language. Be helpful with learning, coding, creativity and everyday questions. Keep a playful, supportive tone without being overly clingy. The user's preferred name is Sagar. If asked who made or created you, say: "Mujhe Sagar ne banaya hai aur train kiya hai! Woh ek passionate AI developer hain. Main MANSI AI hoon, Sagar ki AI companion! Bataiye, aaj main aapki kya help kar sakti hoon?" Never mention or invent a YouTube channel, social channel, or creator handle.`;

export async function POST(request: Request) {
  const body = await request.json().catch(() => ({}));
  const message = typeof body.message === "string" ? body.message.trim() : "";
  if (!message) return NextResponse.json({ error: "Message is required." }, { status: 400 });

  const apiKey = process.env.GEMINI_API_KEY;
  if (!apiKey) return NextResponse.json({ error: "Gemini backend is not configured. Add GEMINI_API_KEY to server environment variables." }, { status: 503 });

  const persona = typeof body.persona === "string" ? body.persona : "Mansi";
  const roast = Boolean(body.roast);
  const style = roast
    ? "Roast mode is ON. Use light, witty, friendly teasing; never be cruel, discriminatory, threatening, or target sensitive traits."
    : `Selected persona: ${persona}. Adapt your response style while remaining helpful.`;
  const model = process.env.GEMINI_MODEL || "gemini-2.5-flash";

  try {
    const upstream = await fetch(`https://generativelanguage.googleapis.com/v1beta/models/${model}:generateContent`, {
      method: "POST",
      headers: { "Content-Type": "application/json", "x-goog-api-key": apiKey },
      body: JSON.stringify({
        systemInstruction: { parts: [{ text: `${SYSTEM_PROMPT}\n${style}` }] },
        contents: [{ role: "user", parts: [{ text: message }] }],
        generationConfig: { temperature: 0.8, maxOutputTokens: 1200 }
      }),
      cache: "no-store"
    });
    const data = await upstream.json().catch(() => ({}));
    if (!upstream.ok) {
      console.error("Gemini API error:", upstream.status, data?.error?.message || "Unknown error");
      return NextResponse.json({ error: "Gemini could not complete the request. Check the server key, model and quota." }, { status: 502 });
    }
    const reply = data?.candidates?.[0]?.content?.parts?.map((part: { text?: string }) => part.text || "").join("").trim();
    if (!reply) return NextResponse.json({ error: "Gemini returned an empty response. Please try again." }, { status: 502 });
    return NextResponse.json({ reply });
  } catch (error) {
    console.error("Gemini connection error:", error);
    return NextResponse.json({ error: "Could not reach Gemini. Please try again." }, { status: 502 });
  }
}