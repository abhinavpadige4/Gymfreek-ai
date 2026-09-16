"""PulseForm AI service (Gymfreek-ai repo, spec section 9).

Runs separately from Next.js. Receives structured JSON only, never video.
Next.js -> FastAPI -> OpenRouter. Run: uvicorn main:app --port 8000
"""

from fastapi import FastAPI

from routers.analyze import router as analyze_router

app = FastAPI(title='pulseform-ai')
app.include_router(analyze_router)


@app.get('/health')
def health() -> dict[str, str]:
    return {'status': 'ok'}
