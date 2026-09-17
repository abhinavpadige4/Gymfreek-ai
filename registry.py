"""Exercise registry: metadata per movement. The browser form engine owns the
rep/angle math; the registry only describes what to coach and demo."""

REGISTRY: dict[str, dict] = {
    'squat': {
        'id': 'squat',
        'name': 'Squat',
        'muscles': ['QUADS', 'GLUTES'],
        'cues': ['Chest up', 'Knees track over toes', 'Depth below parallel'],
        'demoVideoUrl': None,
    },
    'pushup': {
        'id': 'pushup',
        'name': 'Push-Up',
        'muscles': ['CHEST', 'TRICEPS'],
        'cues': ['Body in one line', 'Chest to deck', 'Lock out fully'],
        'demoVideoUrl': None,
    },
    'lunge': {
        'id': 'lunge',
        'name': 'Lunge',
        'muscles': ['QUADS', 'GLUTES'],
        'cues': ['Vertical shin on lead leg', 'Soft rear-knee tap', 'Drive through front heel'],
        'demoVideoUrl': None,
    },
    'kettlebell-swing': {
        'id': 'kettlebell-swing',
        'name': 'Kettlebell Swing',
        'muscles': ['HAMSTRINGS', 'GLUTES', 'LOWER_BACK'],
        'cues': ['Aggressive hip snap', 'Glutes squeezed at apex', 'Bell floats, arms guide'],
        'demoVideoUrl': None,
    },
    'thruster': {
        'id': 'thruster',
        'name': 'Dumbbell Thruster',
        'muscles': ['QUADS', 'SHOULDERS_FRONT'],
        'cues': ['Full squat depth', 'Explode through heels', 'Punch overhead in one motion'],
        'demoVideoUrl': None,
    },
    'deadlift': {
        'id': 'deadlift',
        'name': 'Deadlift',
        'muscles': ['HAMSTRINGS', 'GLUTES', 'LOWER_BACK'],
        'cues': ['Flat back', 'Push the floor away', 'Hips and chest rise together'],
        'demoVideoUrl': None,
    },
    'burpee': {
        'id': 'burpee',
        'name': 'Burpee',
        'muscles': ['CHEST', 'QUADS'],
        'cues': ['Chest to deck', 'Snap feet wide', 'Explosive jump with clap'],
        'demoVideoUrl': None,
    },
    'farmers-carry': {
        'id': 'farmers-carry',
        'name': "Farmer's Carry",
        'muscles': ['FOREARMS', 'BACK_THICKNESS'],
        'cues': ['Crush the handles', 'Shoulders down and back', 'Deliberate heel-to-toe paces'],
        'demoVideoUrl': None,
    },
}


def get_exercise(exercise_id: str) -> dict | None:
    return REGISTRY.get(exercise_id.strip().lower().replace(' ', '-').replace('_', '-'))
