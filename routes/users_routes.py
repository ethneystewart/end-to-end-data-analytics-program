from fastapi import APIRouter

router = APIRouter()

#get all users
@router.post("/users")
def create_user():
    return {"message": "create user"}

# get a specific user by id
@router.get("/users/{user_id}")
def get_user(user_id: int):
    return {"message": f"get user {user_id}"}