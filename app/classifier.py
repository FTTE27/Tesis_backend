import numpy as np
import tensorflow as tf
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
from io import BytesIO
from PIL import Image

class ImageClassifier:
    def __init__(self, model_path, class_names):
        self.model_path = model_path
        self.model = load_model(model_path, compile=False)
        self.class_names = class_names

    def preprocess_image(self, img_bytes, target_size=(224, 224)):
        img = Image.open(BytesIO(img_bytes)).convert("RGB")
        img = img.resize(target_size)
        img_array = image.img_to_array(img)
        img_array = np.expand_dims(img_array, axis=0)
        img_array = tf.keras.applications.densenet.preprocess_input(img_array)
        return img_array

    def predict(self, img_bytes):
        img_array = self.preprocess_image(img_bytes)
        predictions = self.model.predict(img_array)
        probabilities = predictions[0]

        predicted_class_idx = np.argmax(probabilities)
        predicted_class = self.class_names[predicted_class_idx]

        return {
            "predicted_class": predicted_class,
            "probabilities": {
                self.class_names[i]: float(probabilities[i]) for i in range(len(self.class_names))
            }
        }
