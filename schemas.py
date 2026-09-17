"""Pydantic contracts. Structured JSON in, structured JSON out - never video."""

from pydantic import BaseModel, Field


class WorkoutSummaryIn(BaseModel):
    exercise: str = Field(min_length=1, max_length=80)
    totalReps: int = Field(ge=0, le=100000)
    goodReps: int = Field(ge=0, le=100000)
    badReps: int = Field(ge=0, le=100000)
    averageScore: float = Field(ge=0, le=100)
    issues: dict[str, int] = Field(default_factory=dict)
    duration: int = Field(default=0, ge=0, le=86400)


class CoachOut(BaseModel):
    summary: str
    strengths: list[str] = Field(default_factory=list)
    improvements: list[str] = Field(default_factory=list)
    nextWorkoutAdvice: str = ''
    voiceMessage: str = ''


class AnalyzeOut(BaseModel):
    exercise: str
    quality: str  # solid | needs_work | poor
    averageScore: float
    mainIssue: str | None = None
    reps: int


class VoiceIn(BaseModel):
    text: str = Field(min_length=1, max_length=2000)


class VoiceOut(BaseModel):
    text: str
    audioUrl: str | None = None


class Landmark(BaseModel):
    x: float
    y: float
    visibility: float | None = None


class PoseIn(BaseModel):
    # One frame of BlazePose landmarks (33 for full pose; only the 8 the
    # geometry reads are required to be present at their indices).
    landmarks: list[Landmark] = Field(min_length=29)


class PoseOut(BaseModel):
    visible: bool
    kneeAngle: float
    torsoLean: float
    kneeDrift: float
