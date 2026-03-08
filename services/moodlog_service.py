moodlogs = []
next_id = 1


def get_moodlogs():
    return moodlogs


def create_moodlog(payload):
    global next_id

    new_moodlog = {
        "id": next_id,
        "date": payload.date,
        "sleepHours": payload.sleepHours,
        "energyLevels": payload.energyLevels,
        "activities": payload.activities,
        "tags": payload.tags
    }

    next_id += 1
    moodlogs.append(new_moodlog)

    return new_moodlog