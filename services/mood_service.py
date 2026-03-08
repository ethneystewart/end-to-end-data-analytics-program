moods = []

def create_mood(payload):

    new_mood = {
        "id": len(moods) + 1,
        "mood": payload.mood,
        "sentiment": payload.sentiment,
        "moodlog_id": payload.moodlog_id
    }

    moods.append(new_mood)

    return new_mood