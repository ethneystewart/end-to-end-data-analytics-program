import logging
import time

from fastapi import FastAPI, Request

from app.routes.users_routes import router as users_router
from app.routes.moodlogs_routes import router as moodlogs_router
from app.routes.moods_routes import router as moods_router
from app.routes.reflections_routes import router as reflections_router

app = FastAPI()

# logging setup (basic + readable)
# records what requests hit your API and how long they take 

#this is how the logs will appear in console 
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
    force=True,  # reconfigure handlers even if uvicorn set them first
)

logger = logging.getLogger("uvicorn.error") # creates logger 

#most important part registers HTTP middleware (code that runs before and after every request)
@app.middleware("http")
async def log_requests(request: Request, call_next):
    start = time.perf_counter() #records start time 

    #getting the client IP 
    client_host = request.client.host if request.client else "unknown"
    # when request starts 
    logger.info("Started %s %s from %s", request.method, request.url.path, client_host)
    #call the actual route 
    response = await call_next(request)
    #calculate how long it took 
    duration_ms = (time.perf_counter() - start) * 1000
    #log completion 
    logger.info(
        "Completed %s %s -> %s (%.2fms)",
        request.method,
        request.url.path,
        response.status_code,
        duration_ms,
    )
    return response

@app.get("/hello")
def say_hello():
    return {"message": "hello"}

app.include_router(users_router)
app.include_router(moodlogs_router)
app.include_router(moods_router)
app.include_router(reflections_router)
