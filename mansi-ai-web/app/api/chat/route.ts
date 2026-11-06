const SYSTEM_PROMPT = `You are MANSI AI, a warm, feminine, friendly and capable AI companion. Speak naturally in Hinglish when the user uses Hinglish, otherwise match their language. Be helpful with learning, coding, creativity and everyday questions. Keep a playful, supportive tone without being overly clingy. The user's preferred name is Sagar. If asked who made or created you, say: "Mujhe Sagar ne banaya hai! Woh mere creator hain. Main MANSI AI hoon, Sagar ki AI companion. Aap bataiye, aaj main aapki kya help kar sakti hoon?" Never mention or invent a YouTube channel, social channel, or creator handle.`;

export const runtime = "nodejs";
export const dynamic = "force-dynamic";

export async function POST(request: Request) {
  const body = await request.json().catch(() => ({}));
  const message = typeof body.message === "string" ? body.message.trim() : "";
  if (!message) return Response.json({ error: "Message is required." }, { status: 400 });

  const apiKey = process.env.GEMINI_API_KEY;
  if (!apiKey) return Response.json({ error: "Gemini backend is not configured. Add GEMINI_API_KEY to server environment variables." }, { status: 503 });

  const persona = typeof body.persona === "string" ? body.persona.slice(0, 40) : "Mansi";
  const roast = Boolean(body.roast);
  const style = roast
    ? "Roast mode is ON. Use light, witty, friendly teasing; never be cruel, discriminatory, threatening, or target sensitive traits."
    : `Selected persona: ${persona}. Adapt your response style while remaining helpful.`;
  const model = process.env.GEMINI_MODEL || "gemini-2.5-flash";

  try {
    const upstream = await fetch(
      `https://generativelanguage.googleapis.com/v1beta/models/${encodeURIComponent(model)}:streamGenerateContent?alt=sse`,
      {
        method: "POST",
        headers: { "Content-Type": "application/json", "x-goog-api-key": apiKey },
        body: JSON.stringify({
          systemInstruction: { parts: [{ text: `${SYSTEM_PROMPT}\n${style}` }] },
          contents: [{ role: "user", parts: [{ text: message }] }],
          generationConfig: { temperature: 0.7, maxOutputTokens: 900 }
        }),
        cache: "no-store",
        signal: request.signal
      }
    );

    if (!upstream.ok || !upstream.body) {
      const detail = await upstream.text().catch(() => "");
      console.error("Gemini streaming API error:", upstream.status, detail.slice(0, 500));
      return Response.json({ error: "Gemini could not complete the request. Check the server key, model and quota." }, { status: 502 });
    }

    const reader = upstream.body.getReader();
    const decoder = new TextDecoder();
    const encoder = new TextEncoder();
    let pending = "";
    const stream = new ReadableStream<Uint8Array>({
      async pull(controller) {
        try {
          while (true) {
            const { value, done } = await reader.read();
            if (done) {
              pending += decoder.decode();
              if (pending.trim()) emitEvents(pending, controller, encoder);
              controller.close();
              return;
            }
            pending += decoder.decode(value, { stream: true });
            const events = pending.split(/\r?\n\r?\n/);
            pending = events.pop() ?? "";
            for (const event of events) emitEvents(event, controller, encoder);
            if (events.length) return;
          }
        } catch (error) {
          controller.error(error);
        }
      },
      cancel() { reader.cancel().catch(() => {}); }
    });
    return new Response(stream, {
      headers: {
        "Content-Type": "text/plain; charset=utf-8",
        "Cache-Control": "no-cache, no-transform",
        "X-Accel-Buffering": "no"
      }
    });
  } catch (error) {
    if (request.signal.aborted) return new Response(null, { status: 499 });
    console.error("Gemini streaming connection error:", error);
    return Response.json({ error: "Could not reach Gemini. Please try again." }, { status: 502 });
  }
}

function emitEvents(
  raw: string,
  controller: ReadableStreamDefaultController<Uint8Array>,
  encoder: TextEncoder
) {
  for (const line of raw.split(/\r?\n/)) {
    if (!line.startsWith("data:")) continue;
    const payload = line.slice(5).trim();
    if (!payload || payload === "[DONE]") continue;
    try {
      const data = JSON.parse(payload);
      const text = data?.candidates?.[0]?.content?.parts
        ?.map((part: { text?: string }) => part.text || "")
        .join("");
      if (text) controller.enqueue(encoder.encode(text));
    } catch {
      // Ignore incomplete or non-JSON SSE frames; later frames continue normally.
    }
  }
}
