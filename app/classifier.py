import numpy as np
import tensorflow as tf
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
from io import BytesIO
from PIL import Image
import matplotlib.cm as cm
import base64

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
        return img_array, img

    def predict(self, img_bytes):
        img_array, _ = self.preprocess_image(img_bytes)
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

    def predict_with_heatmap(self, img_bytes):
        img_array, original_img = self.preprocess_image(img_bytes)
        img_array = tf.convert_to_tensor(img_array)

        # --- Paso 1: Obtener la clase predicha ---
        predictions = self.model(img_array, training=False)
        predicted_class = tf.argmax(predictions[0])

        # --- Paso 2: Calcular el saliency map ---
        with tf.GradientTape() as tape:
            tape.watch(img_array)
            predictions = self.model(img_array, training=False)
            loss = predictions[:, predicted_class]

        grads = tape.gradient(loss, img_array)
        grads = tf.reduce_max(tf.abs(grads), axis=-1)[0]  # Saliency por canal máximo
        saliency = (grads - tf.reduce_min(grads)) / (tf.reduce_max(grads) - tf.reduce_min(grads) + 1e-8)
        saliency = saliency.numpy()

        # --- Paso 3: Crear el heatmap en color ---
        heatmap = cm.jet(saliency)[:, :, :3]  # RGB
        heatmap = Image.fromarray((heatmap * 255).astype(np.uint8)).resize(original_img.size)

        # --- Paso 4: Fusionar heatmap con la radiografía ---
        fused = Image.blend(original_img.convert("RGBA"), heatmap.convert("RGBA"), alpha=0.5)

        # --- Paso 5: Convertir imagen fusionada a base64 ---
        buffered = BytesIO()
        fused.save(buffered, format="PNG")
        heatmap_base64 = base64.b64encode(buffered.getvalue()).decode("utf-8")

        return {
            "predicted_class": self.class_names[int(predicted_class)],
            "heatmap": heatmap_base64
        }
