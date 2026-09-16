# Gymfreek-ai — PulseForm AI service

Python + FastAPI side of PulseForm (spec section 9). Companion to the
[Gymfreek](https://github.com/abhinavpadige4/Gymfreek) Next.js app.

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

- `OPENROUTER_API_KEY` — server-side only
- `AI_SERVICE_TOKEN` — shared secret the Next.js app sends as a bearer token
