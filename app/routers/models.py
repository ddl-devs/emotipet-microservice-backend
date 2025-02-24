from pydantic import BaseModel
from datetime import datetime

class CommonRequest(BaseModel):
    species: str|None
    breed: str|None
    weight: float|None
    age: int|None
    gender: str|None

class EmotionAnalysis(BaseModel):
    date: datetime  
    emotion: str
    accuracy: float

class WithEmotion(CommonRequest):
    emotions: list[EmotionAnalysis]  

class IMC(BaseModel):
    species: str|None
    weight: float
    height: float
    breed: str|None
