from fastapi import FastAPI
from app.routers import health, recommendations

app = FastAPI()

app.include_router(health.router)
app.include_router(recommendations.router)
