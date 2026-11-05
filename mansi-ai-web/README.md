# MANSI AI Web — Gemini

Separate Next.js 14 web companion inside the Android repository. It does not change Android app files.

## Run locally
1. Use Node.js 18.17+.
2. From this folder run `npm install`.
3. Copy `.env.example` to `.env.local` and set `GEMINI_API_KEY`.
4. Run `npm run dev`, then open http://localhost:3000.

Get a key at https://aistudio.google.com/app/apikey.

## Deploy to Vercel
Import this GitHub repository and set the Root Directory to `mansi-ai-web`. Add `GEMINI_API_KEY` and optionally `GEMINI_MODEL` in Vercel Project Settings → Environment Variables, then deploy. Keep the key server-side; never use a `NEXT_PUBLIC_` prefix.

## Scope
Includes responsive landing/chat UI, persona selector, Roast Mode and a server-side Gemini route. This starter currently sends single-turn requests. Persistent chat history, login, Android app database sync, voice, payments and production rate limiting are not included. This is separate from the MANSI prompt-to-website-builder feature.