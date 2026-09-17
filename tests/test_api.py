"""Endpoint tests. No LLM keys needed: the no-key path must degrade, never 500."""

import os

os.environ.pop('AI_SERVICE_TOKEN', None)
os.environ.pop('OPENROUTER_API_KEY', None)
os.environ.pop('GROQ_API_KEY', None)

from fastapi.testclient import TestClient  # noqa: E402

from main import app  # noqa: E402

client = TestClient(app)


def frame(knee_deg=90, lean_deg=10):
    """33 synthetic side-view landmarks with an exact knee angle."""
    import math

    pts = [{'x': 0.5, 'y': 0.5, 'visibility': 1.0} for _ in range(33)]
    lean = math.radians(lean_deg)
    pts[11] = {'x': 0.42 + 0.15 * math.tan(lean), 'y': 0.15, 'visibility': 1.0}
    pts[12] = {'x': 0.58 + 0.15 * math.tan(lean), 'y': 0.15, 'visibility': 1.0}
    pts[23] = {'x': 0.42, 'y': 0.3, 'visibility': 1.0}
    pts[24] = {'x': 0.58, 'y': 0.3, 'visibility': 1.0}
    pts[25] = {'x': 0.42, 'y': 0.6, 'visibility': 1.0}
    pts[26] = {'x': 0.58, 'y': 0.6, 'visibility': 1.0}
    t = math.radians(180 - knee_deg)
    ax, ay = 0.5 + 0.3 * math.sin(t), 0.6 + 0.3 * math.cos(t)
    pts[27] = {'x': ax - 0.08, 'y': ay, 'visibility': 1.0}
    pts[28] = {'x': ax + 0.08, 'y': ay, 'visibility': 1.0}
    return pts


def summary():
    return {
        'exercise': 'squat',
        'totalReps': 100,
        'goodReps': 91,
        'badReps': 9,
        'averageScore': 87,
        'issues': {'forwardLean': 7},
        'duration': 43,
    }


def test_health():
    assert client.get('/health').json() == {'status': 'ok'}


def test_analyze_quality_bands():
    assert client.post('/ai/analyze', json=summary()).json()['quality'] == 'solid'
    bad = {**summary(), 'averageScore': 50}
    assert client.post('/ai/analyze', json=bad).json()['quality'] == 'poor'


def test_pose_mirror_matches_browser_math():
    res = client.post('/ai/pose/analyze', json={'landmarks': frame(90)}).json()
    assert res['visible'] is True
    assert res['kneeAngle'] == 90.0
    assert 5 < res['torsoLean'] < 20
    hidden = frame(90)
    hidden[25]['visibility'] = 0.0
    assert client.post('/ai/pose/analyze', json={'landmarks': hidden}).json()['visible'] is False


def test_voice_passthrough():
    res = client.post('/ai/voice', json={'text': 'Keep your chest upright.'}).json()
    assert res['text'] == 'Keep your chest upright.'
    assert res['audioUrl'] is None


def test_exercises_registry():
    names = client.get('/ai/exercises').json()['exercises']
    assert 'squat' in names
    assert client.get('/ai/exercises/squat').status_code == 200
    assert client.get('/ai/exercises/pushup').status_code == 200
    assert client.get('/ai/exercises/bogus-lift').status_code == 404


def test_workout_summary_degrades_without_keys():
    res = client.post('/ai/workout-summary', json=summary())
    assert res.status_code == 200  # deterministic fallback, never 500
    assert 'squat' in res.json()['summary']


def test_rejects_bad_payloads():
    assert client.post('/ai/analyze', json={}).status_code == 422
    assert client.post('/ai/pose/analyze', json={'landmarks': []}).status_code == 422
