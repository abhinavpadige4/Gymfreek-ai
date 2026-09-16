"""AI endpoints (spec section 9). All bodies are structured JSON, never video.

Stubs return the contracted shape until Phase 6/7 fills them in.
"""

from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter(prefix='/ai')


class WorkoutSummaryIn(BaseModel):
    exercise: str
    totalReps: int
    goodReps: int
    badReps: int
    averageScore: float
    issues: dict[str, int] = {}
    duration: int = 0


class CoachOut(BaseModel):
    summary: str
    strengths: list[str] = []
    improvements: list[str] = []
    nextWorkoutAdvice: str = ''
    voiceMessage: str = ''


@router.post('/analyze')
def analyze(payload: dict) -> dict:
    # ponytail: stub until the browser MVP proves out what must move server-side.
    return {'received': payload, 'score': None, 'issues': []}


@router.post('/workout-summary')
def workout_summary(payload: WorkoutSummaryIn) -> CoachOut:
    return CoachOut(
        summary='stub',
        voiceMessage='Workout logged. Keep going.',
    )


@router.post('/coach')
def coach(payload: WorkoutSummaryIn) -> CoachOut:
    return CoachOut(
        summary='stub',
        voiceMessage='Workout logged. Keep going.',
    )


@router.post('/voice')
def voice(payload: dict) -> dict:
    # ponytail: cloud TTS behind this endpoint later; browser SpeechSynthesis first.
    return {'received': payload, 'audioUrl': None}


@router.get('/exercises/{exercise_id}')
def exercise(exercise_id: str) -> dict:
    return {'id': exercise_id, 'analyzer': None}
