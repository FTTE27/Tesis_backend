from keras.models import load_model, Model
import numpy as np
from PIL import Image
import io
import matplotlib.cm as cm
import base64
import tensorflow as tf

class ImageClassifier:
    def __init__(self, model_path: str, class_names=None):
        self.model_path = model_path
        self.model = self._load_model(model_path)
        self.class_names = class_names if class_names else None
        self.last_conv_layer_name = self._find_last_conv_layer()

    def _load_model(self, path: str):
        return load_model(path)

    def _find_last_conv_layer(self):
        # Detecta automáticamente la última capa convolucional.
        for layer in reversed(self.model.layers):
            if "conv" in layer.name:
                return layer.name
        raise ValueError("No se encontró ninguna capa convolucional en el modelo.")

    def preprocess(self, image_bytes: bytes):
        image = Image.open(io.BytesIO(image_bytes)).convert("RGB")
        image = image.resize((224, 224))  
        arr = np.array(image, dtype=np.float32) / 255.0
        arr = np.expand_dims(arr, axis=0)
        return arr, image

    def predict(self, image_bytes: bytes):
        arr, _ = self.preprocess(image_bytes)
        preds = self.model.predict(arr)
        return preds.tolist()

    def make_gradcam_heatmap(self, image_array, pred_index=None):
        grad_model = Model(
            inputs=[self.model.inputs],
            outputs=[self.model.get_layer(self.last_conv_layer_name).output, self.model.output]
        )

        with tf.GradientTape() as tape:
            conv_outputs, predictions = grad_model(image_array)
            if pred_index is None:
                pred_index = tf.argmax(predictions[0])
            class_channel = predictions[:, pred_index]

        grads = tape.gradient(class_channel, conv_outputs)
        pooled_grads = tf.reduce_mean(grads, axis=(0, 1, 2))
        conv_outputs = conv_outputs[0]

        heatmap = tf.reduce_mean(tf.multiply(pooled_grads, conv_outputs), axis=-1)
        heatmap = np.maximum(heatmap, 0) / np.max(heatmap)
        return heatmap.numpy()

    def get_prediction_with_heatmap(self, image_bytes: bytes):
        arr, original_img = self.preprocess(image_bytes)
        preds = self.model.predict(arr)
        pred_class = np.argmax(preds[0])

        # Probabilidades con etiquetas
        if self.class_names:
            probs = {self.class_names[i]: float(preds[0][i]) for i in range(len(preds[0]))}
            predicted_label = self.class_names[pred_class]
        else:
            probs = {str(i): float(preds[0][i]) for i in range(len(preds[0]))}
            predicted_label = str(pred_class)

        # Heatmap automático
        heatmap = self.make_gradcam_heatmap(arr, pred_class)
        heatmap = Image.fromarray(np.uint8(255 * heatmap)).resize(original_img.size)
        heatmap = np.array(heatmap)

        jet = cm.get_cmap("jet")
        heatmap_colored = jet(heatmap / 255.0)[:, :, :3]
        heatmap_colored = Image.fromarray(np.uint8(heatmap_colored * 255))

        # Superponer
        overlay = Image.blend(original_img, heatmap_colored, alpha=0.5)

        # Codificar en base64
        buffered = io.BytesIO()
        overlay.save(buffered, format="PNG")
        encoded_image = base64.b64encode(buffered.getvalue()).decode("utf-8")

        return {
            "predicted_class": predicted_label,
            "probabilities": probs,
            "heatmap": encoded_image
        }
