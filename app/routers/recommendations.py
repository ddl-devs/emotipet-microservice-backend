from fastapi import APIRouter, Query
from app.services.gemini import generate_response

router = APIRouter()


@router.post("/recommendations/imc")
async def get_recommendations(
    weight: float = Query(..., description="Weight of the dog in kg"),
    height: float = Query(..., description="Height of the dog in cm"),
):
    prompt = f"Calcular o resultado do IMC de uma pessoa com Peso: {weight}kg e Altura: {height}cm. (retorna apenas o valor do IMC e a classificação do resultado)"

    response = generate_response(prompt)

    return {"status": "ok", "response": response.text}
