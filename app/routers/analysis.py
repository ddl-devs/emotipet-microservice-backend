import io
import logging

from app.services.image_processor import dog_process_image, cat_process_image

from fastapi import File, UploadFile, HTTPException
from fastapi.routing import APIRouter
from PIL import Image

router = APIRouter()

logging.basicConfig(level=logging.INFO)

@router.post("/dog-emotion-predict")
async def dog_emotion_predict(image: UploadFile = File(...)):
    try:
        image_data = await image.read()
        image_pil = Image.open(io.BytesIO(image_data))

        result = dog_process_image(image_pil)
        return result
    except Exception as e:
        logging.error(f"Erro ao processar a imagem: {e}")
        raise HTTPException(status_code=500, detail=f"Erro ao processar a imagem: {e}")

@router.post("/cat-emotion-predict")
async def cat_emotion_predict(image: UploadFile = File(...)):
    try:
        image_data = await image.read()
        image_pil = Image.open(io.BytesIO(image_data))

        result = cat_process_image(image_pil)
        return result
    except Exception as e:
        logging.error(f"Erro ao processar a imagem: {e}")
        raise HTTPException(status_code=500, detail=f"Erro ao processar a imagem: {e}")
