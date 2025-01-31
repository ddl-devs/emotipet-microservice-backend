from fastapi import APIRouter, Query
from app.services.gemini import generate_response

router = APIRouter()


@router.post("/recommendations/imc")
async def get_imcc_recommendations(
    weight: float = Query(..., description="Weight of the dog in kg"),
    height: float = Query(..., description="Height of the dog in cm"),
):
    prompt = (
        f"Calcule o IMCC (Índice de Massa Corporal Canino) para um cachorro com "
        f"peso de {weight} kg e altura de {height} cm. Retorne apenas o valor do IMCC e sua classificação.\n\n"
        "A fórmula para o cálculo é:\n"
        "IMCC = peso / (altura × altura)\n\n"
        "Classificação:\n"
        "- Abaixo do peso: IMCC < 18.5\n"
        "- Peso normal: 18.5 ≤ IMCC < 25\n"
        "- Acima do peso: 25 ≤ IMCC < 30\n"
        "- Obeso: IMCC ≥ 30"
    )

    response = generate_response(prompt)

    return {"status": "ok", "response": response.text}


@router.post("/recommendations/activities")
async def get_activities_recommendations(
    weight: float = Query(..., description="Weight of the dog in kg"),
    breed: str = Query(..., description="Breed of the dog"),
    age: int = Query(..., description="Age of the dog in years"),
):
    prompt = (
        f"Recomende atividades físicas para um cachorro da raça {breed} com {weight} kg e {age} anos de idade. "
        "As atividades devem ser adequadas para o porte e a faixa etária do cachorro, "
        "considerando o seu nível de energia e condição física.\n\n"
        "Considerações: cachorros mais velhos podem precisar de atividades mais leves, "
        "enquanto cachorros jovens podem se beneficiar de atividades mais intensas."
    )

    response = generate_response(prompt)

    return {"status": "ok", "response": response.text}


@router.post("/recommendations/health")
async def get_health_wealness_recommendations(
    weight: float = Query(..., description="Weight of the dog in kg"),
    breed: str = Query(..., description="Breed of the dog"),
    age: int = Query(..., description="Age of the dog in years"),
):
    prompt = (
        f"Recomende cuidados de saúde e bem-estar para um cachorro da raça {breed} com {age} anos e {weight} kg. "
        "As recomendações devem levar em consideração a raça e o peso do cachorro, "
        "incluindo cuidados preventivos, alimentação e quaisquer condições específicas da raça.\n\n"
        "Por exemplo, algumas raças podem ter propensão a problemas articulares ou cardíacos."
    )

    response = generate_response(prompt)

    return {"status": "ok", "response": response.text}


@router.post("/recommendations/training")
async def get_training_recommendations(
    weight: float = Query(..., description="Weight of the dog in kg"),
    breed: str = Query(..., description="Breed of the dog"),
    age: float = Query(..., description="Age of the dog in years"),
):
    prompt = (
        f"Recomende dicas de treinamento e comportamento para um cachorro da raça {breed} com {age} anos e {weight} kg. "
        "As recomendações devem incluir técnicas de adestramento para corrigir comportamentos indesejados, "
        "estimulação mental e socialização.\n\n"
        "Leve em conta que raças diferentes podem ter necessidades distintas de treinamento e comportamento."
    )

    response = generate_response(prompt)

    return {"status": "ok", "response": response.text}


@router.post("/recommendations/products")
async def get_products_recommendations(
    weight: float = Query(..., description="Weight of the dog in kg"),
    breed: str = Query(..., description="Breed of the dog"),
    age: float = Query(..., description="Age of the dog in years"),
):
    prompt = (
        f"Recomende produtos para um cachorro da raça {breed} com {age} anos e {weight} kg."
        "Os produtos podem incluir ração, brinquedos, acessórios, camas e outros itens adequados ao porte e necessidades do cachorro.\n\n"
        "Leve em consideração a saúde e a preferência do cachorro ao sugerir os produtos."
    )

    response = generate_response(prompt)

    return {"status": "ok", "response": response.text}
