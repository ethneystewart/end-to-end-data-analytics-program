from fastapi import APIRouter

router = APIRouter()

#get all moods 
@router.get("/moods")
def get_moods():
    return {"message": "list moods"}

#create a new mood 
@router.post("/moods")
def create_mood():
    return {"message": "create mood"}