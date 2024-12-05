from fastapi import APIRouter
from app.services.image_processor import process_image

router = APIRouter()

#example route
@router.get("/health")
async def health_check():
    return {"status": "ok"}


@router.get("/test")
async def test_emotional_model():
    return process_image('./models/test.jpg')