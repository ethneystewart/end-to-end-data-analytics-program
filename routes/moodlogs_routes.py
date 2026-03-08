from fastapi import APIRouter

router = APIRouter()

# get all mood logs 
@router.get("/moodlogs")
def get_moodlogs():
    return {"message": "return all mood logs"}

# get a specific mood log by id 
@router.get("/moodlogs/{moodlog_id}")
def get_moodlog(moodlog_id: int):
    return {"message": f"return mood log {moodlog_id}"}

#create a new mood log 
@router.post("/moodlogs")
def create_moodlog():
    return {"message": "create a new mood log"}

#delete a mood log by id
@router.delete("/moodlogs/{moodlog_id}")
def delete_moodlog(moodlog_id: int):
    return {"message": f"delete mood log {moodlog_id}"}