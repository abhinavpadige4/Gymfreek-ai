"""Joint-angle geometry over BlazePose landmarks.

Exact mirror of the browser engine (frontend lib/form-engine/angles.ts):
same indices, same formulas, same thresholds. The browser stays the
real-time path; this mirror exists so the service can validate frames and
so both sides can be tested against identical numbers.
"""

import math

# BlazePose indices we need.
LM = {
    'leftShoulder': 11,
    'rightShoulder': 12,
    'leftHip': 23,
    'rightHip': 24,
    'leftKnee': 25,
    'rightKnee': 26,
    'leftAnkle': 27,
    'rightAnkle': 28,
}


def mid(a: dict, b: dict) -> dict:
    return {'x': (a['x'] + b['x']) / 2, 'y': (a['y'] + b['y']) / 2}


def angle_at(a: dict, b: dict, c: dict) -> float:
    """Angle at vertex b between a-b-c, in degrees 0..180."""
    v1x, v1y = a['x'] - b['x'], a['y'] - b['y']
    v2x, v2y = c['x'] - b['x'], c['y'] - b['y']
    m1, m2 = math.hypot(v1x, v1y), math.hypot(v2x, v2y)
    if m1 == 0 or m2 == 0:
        return 180.0
    cos = min(1.0, max(-1.0, (v1x * v2x + v1y * v2y) / (m1 * m2)))
    return math.degrees(math.acos(cos))


def knee_angle(lm: list) -> float:
    """Knee flexion from averaged sides. Standing ~170, deep squat ~70."""
    hip = mid(lm[LM['leftHip']], lm[LM['rightHip']])
    knee = mid(lm[LM['leftKnee']], lm[LM['rightKnee']])
    ankle = mid(lm[LM['leftAnkle']], lm[LM['rightAnkle']])
    return angle_at(hip, knee, ankle)


def torso_lean(lm: list) -> float:
    """Torso lean from vertical, degrees. Upright ~0-15, heavy lean 45+."""
    shoulder = mid(lm[LM['leftShoulder']], lm[LM['rightShoulder']])
    hip = mid(lm[LM['leftHip']], lm[LM['rightHip']])
    dx, dy = shoulder['x'] - hip['x'], shoulder['y'] - hip['y']
    length = math.hypot(dx, dy) or 1.0
    return math.degrees(math.acos(min(1.0, abs(dy) / length)))


def knee_drift(lm: list) -> float:
    """Knee-vs-ankle horizontal drift over hip width. > ~0.35 = caving in."""
    hip_w = abs(lm[LM['leftHip']]['x'] - lm[LM['rightHip']]['x']) or 1.0
    knee = mid(lm[LM['leftKnee']], lm[LM['rightKnee']])
    ankle = mid(lm[LM['leftAnkle']], lm[LM['rightAnkle']])
    return abs(knee['x'] - ankle['x']) / hip_w


def landmarks_visible(lm: list) -> bool:
    return all((lm[i].get('visibility', 1) or 0) >= 0.5 for i in LM.values())
