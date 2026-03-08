reflections = []

def create_reflection(payload):

    new_reflection = {
        "id": len(reflections) + 1,
        "moodlog_id": payload.moodlog_id,
        "reflection": payload.reflection
    }

    reflections.append(new_reflection)

    return new_reflection