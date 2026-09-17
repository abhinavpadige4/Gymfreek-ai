"""OpenRouter primary + Groq fallback on structured summaries. Never video, never per-frame.

No key or any provider failure -> deterministic fallback summary, never a 500.
Free-tier defaults, verified live 2026-09-17 (both return valid coach JSON).
"""

import json
import logging
import os

import httpx

from schemas import CoachOut, WorkoutSummaryIn

log = logging.getLogger('gymfreek-ai')

OPENROUTER_MODEL = os.environ.get(
    'OPENROUTER_MODEL', 'nvidia/nemotron-3-super-120b-a12b:free'
)
GROQ_MODEL = os.environ.get('GROQ_MODEL', 'openai/gpt-oss-120b')

SYSTEM_PROMPT = (
    'You are Gymfreek, an evidence-based strength and conditioning coach. '
    'You receive a JSON workout summary (exercise, reps, scores, issue counts). '
    'Reply with JSON ONLY, exactly this shape: '
    '{"summary": str, "strengths": [str], "improvements": [str], '
    '"nextWorkoutAdvice": str, "voiceMessage": str}. '
    'voiceMessage is one short spoken cue (under 25 words). No markdown, no extra keys.'
)


def fallback_coaching(payload: WorkoutSummaryIn) -> CoachOut:
    top_issue = max(payload.issues, key=lambda k: payload.issues[k], default=None)
    good_rate = payload.goodReps / max(1, payload.totalReps)
    if good_rate >= 0.9 and payload.averageScore >= 85:
        summary = f'Strong {payload.exercise} session: {payload.goodReps}/{payload.totalReps} clean reps.'
    elif good_rate >= 0.7:
        summary = f'Solid {payload.exercise} volume with room to tighten form.'
    else:
        summary = f'Tough {payload.exercise} session - form broke down, prioritize quality next time.'
    improvements = [f'Address {top_issue} first.'] if top_issue else ['Keep every rep clean.']
    return CoachOut(
        summary=summary,
        strengths=[f'{payload.goodReps} clean reps at {payload.averageScore:.0f} average.']
        if payload.totalReps
        else [],
        improvements=improvements,
        nextWorkoutAdvice='Repeat the same circuit; stop one rep before form slips.',
        voiceMessage=f'{payload.exercise} done. {improvements[0]}',
    )


async def openrouter_coaching(payload: WorkoutSummaryIn) -> CoachOut:
    attempts: list[tuple[str, dict[str, str], dict]] = []
    if os.environ.get('OPENROUTER_API_KEY', ''):
        attempts.append(
            (
                'https://openrouter.ai/api/v1/chat/completions',
                {
                    'Authorization': f"Bearer {os.environ['OPENROUTER_API_KEY']}",
                    'Content-Type': 'application/json',
                    'HTTP-Referer': os.environ.get('OPENROUTER_APP_URL', ''),
                    'X-Title': os.environ.get('OPENROUTER_APP_NAME', 'Gymfreek'),
                },
                {'model': OPENROUTER_MODEL},
            )
        )
    if os.environ.get('GROQ_API_KEY', ''):
        attempts.append(
            (
                'https://api.groq.com/openai/v1/chat/completions',
                {
                    'Authorization': f"Bearer {os.environ['GROQ_API_KEY']}",
                    'Content-Type': 'application/json',
                },
                {'model': GROQ_MODEL},
            )
        )
    if not attempts:
        return fallback_coaching(payload)
    body = {
        'messages': [
            {'role': 'system', 'content': SYSTEM_PROMPT},
            {'role': 'user', 'content': payload.model_dump_json()},
        ],
        'temperature': 0.4,
        'max_tokens': 800,
    }
    # ponytail: prompt-only JSON, no response_format - verified on both free
    # models; response_format breaks compat with some OpenRouter free models.
    try:
        async with httpx.AsyncClient(timeout=60) as client:
            for url, headers, model in [(u, h, m['model']) for u, h, m in attempts]:
                try:
                    res = await client.post(
                        url, headers=headers, json={**body, 'model': model}
                    )
                    res.raise_for_status()
                    text = res.json()['choices'][0]['message']['content']
                    return CoachOut.model_validate(json.loads(text))
                except Exception as exc:
                    log.warning('%s failed (%s) - trying next.', url, type(exc).__name__)
    except Exception as exc:  # network down entirely - degrade, never crash
        log.warning('LLM unreachable (%s) - using fallback.', type(exc).__name__)
    return fallback_coaching(payload)
