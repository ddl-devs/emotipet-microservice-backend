from workers.consumer import poll_queue
from fastapi import FastAPI
from routers.recommendations import router
from contextlib import asynccontextmanager
import asyncio

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Runs SQS listener in the background"""
    task = asyncio.create_task(poll_queue())  
    yield
    task.cancel()

    try:
        await task
    except asyncio.CancelledError:
        pass

app = FastAPI(lifespan=lifespan)

app.include_router(router)