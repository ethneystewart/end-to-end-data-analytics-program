from fastapi import APIRouter

router = APIRouter()

# create a new reflection
@router.post("/reflections")
def create_reflection():
    return {"message": "create reflection"}

#get reflections for a specific mood log
@router.get("/reflections/{moodlog_id}")
def get_reflections(moodlog_id: int):
    return {"message": f"get reflections for mood log {moodlog_id}"}