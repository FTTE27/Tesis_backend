import numpy as np
import tensorflow as tf
from tensorflow.keras.models import load_model, Model
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
        self.last_conv_layer_name = self._find_last_conv_layer()
        
    def _find_last_conv_layer(self):
        """
        Busca automáticamente la última capa convolucional en DenseNet201.
        """
        for layer in reversed(self.model.layers):
            if isinstance(layer, tf.keras.layers.Conv2D):
                return layer.name
        raise ValueError("No se encontró ninguna capa convolucional en DenseNet201.")

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

    def make_gradcam_heatmap(self, img_array, predicted_class_idx):
        grad_model = Model(
            inputs=self.model.input,
            outputs=[self.model.get_layer(self.last_conv_layer_name).output, self.model.output]
        )

        with tf.GradientTape() as tape:
            conv_outputs, predictions = grad_model(img_array)

            # Forzar a que predictions sea tensor
            if isinstance(predictions, (list, tuple)):
                predictions = predictions[0]

            # Calcular la pérdida sobre la clase predicha
            loss = predictions[:, predicted_class_idx]

        grads = tape.gradient(loss, conv_outputs)
        pooled_grads = tf.reduce_mean(grads, axis=(0, 1, 2))

        conv_outputs = conv_outputs[0]
        heatmap = tf.reduce_sum(tf.multiply(pooled_grads, conv_outputs), axis=-1)
        heatmap = tf.maximum(heatmap, 0)
        heatmap = heatmap / (tf.reduce_max(heatmap) + 1e-8)
        return heatmap.numpy()


    def overlay_heatmap(self, heatmap, original_img, alpha=0.5, colormap="jet"):
        """
        Superpone el heatmap sobre la imagen original.
        """
        # Redimensionar heatmap al tamaño de la imagen original
        heatmap = tf.image.resize(
            heatmap[..., np.newaxis],  # Añadimos dimensión de canal
            (original_img.size[1], original_img.size[0])
        )
        heatmap = tf.squeeze(heatmap).numpy()

        # Aplicar colormap
        jet = cm.get_cmap(colormap)
        heatmap_colored = jet(heatmap)[:, :, :3]
        heatmap_colored = (heatmap_colored * 255).astype(np.uint8)
        heatmap_img = Image.fromarray(heatmap_colored).convert("RGBA")

        # Convertir original a RGBA y fusionar
        original_img_rgba = original_img.convert("RGBA")
        superimposed = Image.blend(original_img_rgba, heatmap_img, alpha=alpha)
        return superimposed

    def predict_heatmap(self, img_bytes):
        try:
            img_array, original_img = self.preprocess_image(img_bytes)

            predictions = self.model.predict(img_array)

            # Forzar predictions a tensor
            if isinstance(predictions, (list, tuple)):
                predictions = predictions[0]

            predicted_class_idx = np.argmax(predictions)
            predicted_class = self.class_names[predicted_class_idx]

            heatmap = self.make_gradcam_heatmap(img_array, predicted_class_idx)
            superimposed = self.overlay_heatmap(heatmap, original_img, alpha=0.5)

            buffered = BytesIO()
            superimposed.save(buffered, format="PNG")
            heatmap_base64 = base64.b64encode(buffered.getvalue()).decode("utf-8")

            return {
                "predicted_class": predicted_class,
                "heatmap": heatmap_base64
            }

        except Exception as e:
            raise Exception(f"Error procesando la imagen: {str(e)}")
