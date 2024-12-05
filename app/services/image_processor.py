import tensorflow as tf
from app.config import settings
import numpy as np


def custom_depthwise_conv2d(*args, **kwargs):
    kwargs.pop('groups', None)  
    return tf.keras.layers.DepthwiseConv2D(*args, **kwargs)


def prepare_image(img_path: str):
    img = tf.keras.utils.load_img(img_path, target_size=(224, 224))  
    img_array = tf.keras.utils.img_to_array(img)  
    img_array = np.expand_dims(img_array, axis=0) 
    img_array /= 255.0

    return img_array



def process_image(image_path: str):

    model = tf.keras.models.load_model(
        settings.emotional_model_path,
        compile=False, 
        custom_objects={'DepthwiseConv2D': custom_depthwise_conv2d}
    )

    img_array = prepare_image(image_path)
    
    predictions = model.predict(img_array)

    predicted_class_index = np.argmax(predictions)

    print(f"Probabilidades para as classes: {predictions}")

    class_names = ['Angry', 'Sad', 'happy'] 
    predicted_class = class_names[predicted_class_index]
    
    return {
        "result": predicted_class
    }