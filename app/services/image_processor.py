from pathlib import Path
import logging
from PIL import Image
import numpy as np
import tensorflow as tf
from tensorflow.keras.models import load_model
from tensorflow.keras.applications.mobilenet import preprocess_input

# Configuração do logger
logging.basicConfig(level=logging.INFO)


def custom_depthwise_conv2d(*args, **kwargs):
    kwargs.pop("groups", None)
    return tf.keras.layers.DepthwiseConv2D(*args, **kwargs)


class FixedDropout(tf.keras.layers.Dropout):
    def __init__(self, rate, **kwargs):
        super().__init__(rate, **kwargs)


def prepare_image(img: Image.Image) -> np.ndarray:
    if img.mode != "RGB":
        img = img.convert("RGB")

    img = img.resize((224, 224))
    img_array = tf.keras.utils.img_to_array(img)
    img_array = np.expand_dims(img_array, axis=0)
    return preprocess_input(img_array)


def dog_process_image(image_path: str):
    model_path = Path("models/dog_model.h5")

    if not model_path.exists():
        raise FileNotFoundError(f"Modelo não encontrado em: {model_path}")

    custom_objects = {
        "DepthwiseConv2D": custom_depthwise_conv2d,
        "FixedDropout": FixedDropout,
    }

    try:
        model = load_model(model_path, compile=False, custom_objects=custom_objects)
    except Exception as e:
        logging.error(f"Erro ao carregar o modelo: {e}")
        raise RuntimeError(f"Erro ao carregar o modelo: {e}")

    img_array = prepare_image(image_path)

    predictions = model.predict(img_array)
    predicted_class_index = np.argmax(predictions)

    class_names = ["angry", "happy", "relaxed", "sad"]
    predicted_class = class_names[predicted_class_index]

    return {"result": predicted_class}
