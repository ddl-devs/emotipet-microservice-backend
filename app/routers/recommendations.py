from fastapi import APIRouter, Query
from services.gemini import generate_response
from pydantic import BaseModel
from typing import List
from routers.models import (
    IMC,
    CommonRequest,
    WithEmotion,
)

router = APIRouter()


@router.post("/recommendations/imc")
async def get_imcc_recommendations(
    bodyImc: IMC
):
    prompt = (
        f"Calcule o IMC (Índice de Massa Corporal) para um {bodyImc.species} da raça {bodyImc.breed}"
        f" com peso de {bodyImc.weight} kg e altura de {bodyImc.height} cm. Retorne apenas o valor do IMC e sua classificação.\n\n"
        "Seja breve e objetivo na resposta, fornecendo informações claras e concisas."
    )

    response = generate_response(prompt) 
    return {"status": "ok", "response": response.text}


@router.post("/recommendations/activities")
async def get_activities_recommendations(
    bodyEmotion: WithEmotion
):
    prompt = (
        f"Recomende atividades físicas para um {bodyEmotion.species} da raça {bodyEmotion.breed} com {bodyEmotion.weight} kg e {bodyEmotion.age} anos de idade. "
        f"As atividades devem ser adequadas para o porte e a faixa etária do {bodyEmotion.species}, "
        "considerando o seu nível de energia e condição física.\n\n"
        f"Considerações: {bodyEmotion.species}s mais velhos podem precisar de atividades mais leves, "
        f"enquanto {bodyEmotion.species}s jovens podem se beneficiar de atividades mais intensas."
    )

    if bodyEmotion.emotions:
                prompt += f"Além disso, considere as análises emocionais recentes do {bodyEmotion.species}s para contextualizar a recomendação de atividades.\n"
                prompt += "Cada análise tem um nível de precisão e data, indicando a confiabilidade do dado:\n"

                for emotion in bodyEmotion.emotions:
                    prompt += (
                        f"- Em {emotion.date}, o pet foi classificado como {emotion.emotion} "
                        f"com uma precisão de {emotion.accuracy:.2f}.\n"
                    )

                prompt += "\nUse essas informações para fornecer uma análise mais completa, levando em conta a confiabilidade dos dados emocionais."


    prompt += "Defina a duração e a frequência das atividades, bem como quaisquer restrições ou recomendações especiais. "
    prompt += "Seja breve e objetivo na resposta, fornecendo informações claras e concisas"

    response = generate_response(prompt)

    return {"status": "ok", "response": response.text}


@router.post("/recommendations/health")
async def get_health_wealness_recommendations(
    bodyEmotion: WithEmotion
):
    prompt = (
        f"Recomende cuidados de saúde e bem-estar para um {bodyEmotion.species} da raça {bodyEmotion.breed} com {bodyEmotion.age} anos e {bodyEmotion.weight} kg. "
        f"As recomendações devem levar em consideração a raça e o peso do {bodyEmotion.species}s, "
        "incluindo cuidados preventivos, alimentação e quaisquer condições específicas da raça.\n\n"
        "Por exemplo, algumas raças podem ter propensão a problemas articulares ou cardíacos."
    )

    if bodyEmotion.emotions:
                prompt += f"Além disso, considere as análises emocionais recentes do {bodyEmotion.species}s para contextualizar as recomendações de cuidados.\n"
                prompt += "Cada análise tem um nível de precisão e data, indicando a confiabilidade do dado:\n"

                for emotion in bodyEmotion.emotions:
                    prompt += (
                        f"- Em {emotion.date}, o pet foi classificado como {emotion.emotion} "
                        f"com uma precisão de {emotion.accuracy:.2f}.\n"
                    )

                prompt += "\nUse essas informações para fornecer uma análise mais completa, levando em conta a confiabilidade dos dados emocionais."
    
    prompt += "Seja breve e objetivo na resposta, fornecendo informações claras e concisas."

    response = generate_response(prompt)

    return {"status": "ok", "response": response.text}


@router.post("/recommendations/training")
async def get_training_recommendations(
    bodyEmotion: WithEmotion
):
    prompt = (
        f"Recomende dicas de treinamento e comportamento para um {bodyEmotion.species} da raça {bodyEmotion.breed} com {bodyEmotion.age} anos e {bodyEmotion.weight} kg. "
        "As recomendações devem incluir técnicas de adestramento para corrigir comportamentos indesejados, "
        "estimulação mental e socialização.\n\n"
        "Leve em conta que raças diferentes podem ter necessidades distintas de treinamento e comportamento."
    )

    if bodyEmotion.emotions:
            prompt += f"Além disso, considere as análises emocionais recentes do {bodyEmotion.species} para contextualizar a avaliação de treinamento.\n"
            prompt += "Cada análise tem um nível de precisão e data, indicando a confiabilidade do dado:\n"

            for emotion in bodyEmotion.emotions:
                prompt += (
                    f"- Em {emotion.date}, o pet foi classificado como {emotion.emotion} "
                    f"com uma precisão de {emotion.accuracy:.2f}.\n"
                )

            prompt += "\nUse essas informações para fornecer uma análise mais completa, levando em conta a confiabilidade dos dados emocionais."

    prompt += "Seja breve e objetivo na resposta, fornecendo informações claras e concisas"

    response = generate_response(prompt)

    return {"status": "ok", "response": response.text}


@router.post("/recommendations/products")
async def get_products_recommendations(
    body: CommonRequest
):
    prompt = (
        f"Recomende produtos para um {body.species} da raça {body.breed} com {body.age} anos e {body.weight} kg."
        f"Os produtos podem incluir ração, brinquedos, acessórios, camas e outros itens adequados ao porte e necessidades do {body.species}.\n\n"
        f"Leve em consideração a saúde e a preferência do {body.species} ao sugerir os produtos."
    )

    prompt += "Seja breve e objetivo na resposta, fornecendo informações claras e concisas"

    response = generate_response(prompt)

    return {"status": "ok", "response": response.text}
