from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    emotional_model_path : str = "./models/keras_model.h5"

settings = Settings()