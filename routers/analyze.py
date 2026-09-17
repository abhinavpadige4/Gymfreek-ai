"""AI endpoints. Structured JSON in/out - never video, never per-frame."""

from fastapi import APIRouter, Depends, HTTPException

from auth import require_service_token
from geometry import knee_angle, knee_drift, landmarks_visible, torso_lean
from llm import fallback_coaching, openrouter_coaching
from registry import REGISTRY, get_exercise
from schemas import (
    AnalyzeOut,
    CoachOut,
    PoseIn,
    PoseOut,
    VoiceIn,
    VoiceOut,
    WorkoutSummaryIn,
)

router = APIRouter(prefix='/ai')


@router.post('/pose/analyze', response_model=PoseOut)
async def pose_analyze(
    payload: PoseIn, _auth: None = Depends(require_service_token)
) -> PoseOut:
    # Rule-based landmark mirror of the browser engine. Accepts one frame of
    # landmarks (never an image) for validation and future server-side checks.
    lm = [p.model_dump() for p in payload.landmarks]
    if not landmarks_visible(lm):
        return PoseOut(visible=False, kneeAngle=180.0, torsoLean=0.0, kneeDrift=0.0)
    return PoseOut(
        visible=True,
        kneeAngle=round(knee_angle(lm), 1),
        torsoLean=round(torso_lean(lm), 1),
        kneeDrift=round(knee_drift(lm), 3),
    )


@router.post('/analyze', response_model=AnalyzeOut)
async def analyze(
    payload: WorkoutSummaryIn, _auth: None = Depends(require_service_token)
) -> AnalyzeOut:
    top_issue = max(payload.issues, key=lambda k: payload.issues[k], default=None)
    if payload.averageScore >= 85:
        quality = 'solid'
    elif payload.averageScore >= 65:
        quality = 'needs_work'
    else:
        quality = 'poor'
    return AnalyzeOut(
        exercise=payload.exercise,
        quality=quality,
        averageScore=payload.averageScore,
        mainIssue=top_issue,
        reps=payload.totalReps,
    )


@router.post('/workout-summary', response_model=CoachOut)
async def workout_summary(
    payload: WorkoutSummaryIn, _auth: None = Depends(require_service_token)
) -> CoachOut:
    return await openrouter_coaching(payload)


@router.post('/coach', response_model=CoachOut)
async def coach(
    payload: WorkoutSummaryIn, _auth: None = Depends(require_service_token)
) -> CoachOut:
    # Alias kept for the spec's endpoint list; same contract as workout-summary.
    if payload.totalReps == 0 and not payload.issues:
        return fallback_coaching(payload)
    return await openrouter_coaching(payload)


@router.post('/voice', response_model=VoiceOut)
async def voice(payload: VoiceIn, _auth: None = Depends(require_service_token)) -> VoiceOut:
    # ponytail: cloud TTS later; the browser speaks this text today.
    return VoiceOut(text=payload.text)


@router.get('/exercises/{exercise_id}')
async def exercise(
    exercise_id: str, _auth: None = Depends(require_service_token)
) -> dict:
    entry = get_exercise(exercise_id)
    if entry is None:
        raise HTTPException(status_code=404, detail='Unknown exercise.')
    return entry


@router.get('/exercises')
async def exercise_list(_auth: None = Depends(require_service_token)) -> dict:
    return {'exercises': list(REGISTRY.keys())}
