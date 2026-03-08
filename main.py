from fastapi import FastAPI

from routes.users_routes import router as users_router
from routes.moodlogs_routes import router as moodlogs_router
from routes.moods_routes import router as moods_router
from routes.reflections_routes import router as reflections_router

app = FastAPI()

@app.get("/hello")
def say_hello():
    return {"message": "hello"}

app.include_router(users_router)
app.include_router(moodlogs_router)
app.include_router(moods_router)
app.include_router(reflections_router)