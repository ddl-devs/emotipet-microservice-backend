from fastapi import FastAPI
from app.routers import analysis, recommendations

app = FastAPI()

app.include_router(analysis.router)
app.include_router(recommendations.router)
