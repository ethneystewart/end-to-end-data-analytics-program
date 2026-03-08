users = []
next_id = 1


def create_user(payload):
    global next_id

    new_user = {
        "id": next_id,
        "firstName": payload.firstName,
        "lastName": payload.lastName,
        "email": payload.email
    }

    next_id += 1
    users.append(new_user)

    return new_user


def get_user(user_id: int):
    for user in users:
        if user["id"] == user_id:
            return user

    return {"error": "User not found"}