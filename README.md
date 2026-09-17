# Gymfreek-ai — AI service

Python + FastAPI side of Gymfreek. Companion to the
[Gymfreek](https://github.com/abhinavpadige4/Gymfreek) Next.js app. Deployed
separately (Railway/Render/AWS); the two repos connect over HTTPS + bearer
token, they are never merged.

Rule: receives **structured JSON only, never video**. Real-time form stays in
the browser (MediaPipe + rule engine); this service does periodic summaries,
LLM coaching via OpenRouter, and (later) cloud TTS.

## Run

```bash
python -m venv .venv && .venv/Scripts/activate  # Windows
pip install -r requirements.txt
uvicorn main:app --port 8000
```

## Endpoints

- `GET /health`
- `POST /ai/analyze`
- `POST /ai/workout-summary`
- `POST /ai/coach`
- `POST /ai/voice`
- `GET /ai/exercises/{id}`

## Secrets (env, never committed)

- `OPENROUTER_API_KEY` — primary LLM key, server-side only (without any key
  the service returns deterministic fallback coaching, never 500)
- `OPENROUTER_MODEL` — default `nvidia/nemotron-3-super-120b-a12b:free`
- `GROQ_API_KEY` — fallback LLM key, tried after OpenRouter fails
- `GROQ_MODEL` — default `openai/gpt-oss-120b`
- `OPENROUTER_APP_NAME` / `OPENROUTER_APP_URL` — attribution headers
- `AI_SERVICE_TOKEN` — shared secret the Next.js app sends as a bearer token
  (unset = open dev mode with a warning)

## Deploy (separate service)

Railway/Render: Python 3.12, `pip install -r requirements.txt`,
start `uvicorn main:app --host 0.0.0.0 --port $PORT`. Set the four env vars
above, then put the public URL + same `AI_SERVICE_TOKEN` into the Next.js
app as `AI_SERVICE_URL` / `AI_SERVICE_TOKEN`. Payments never touch this
service.
