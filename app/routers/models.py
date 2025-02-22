from pydantic import BaseModel
from datetime import datetime

class CommonRequest(BaseModel):
    breed: str
    weight: float
    age: int

class EmotionAnalysis(BaseModel):
    date: datetime  
    emotion: str
    accuracy: float

class WithEmotion(CommonRequest):
    emotions: list[EmotionAnalysis]  

class IMC(BaseModel):
    weight: float
    height: float
    breed: str
