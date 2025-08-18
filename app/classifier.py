from keras.models import load_model, Model
import numpy as np
from PIL import Image
import io
import matplotlib.cm as cm
import base64
import tensorflow as tf
from tensorflow.keras.applications.densenet import preprocess_input

class ImageClassifier:
    def __init__(self, model_path: str, class_names=None):
        self.model_path = model_path
        self.model = self._load_model(model_path)
        self.class_names = class_names if class_names else ["BAC_PNEUMONIA", "NORMAL", "VIR_PNEUMONIA"]
        self.last_conv_layer_name = self._find_last_conv_layer()
    
    def _load_model(self, path: str):
        return load_model(path, compile=False)
    
    def _find_last_conv_layer(self):
        # Buscar la última capa convolucional en el modelo base DenseNet
        for layer in reversed(self.model.layers):
            if "conv5_block16" in layer.name and "conv" in layer.name:
                return layer.name
        # Fallback si no encontramos la capa específica
        for layer in reversed(self.model.layers[1].layers):
            if "conv" in layer.name:
                return layer.name
        raise ValueError("No se encontró capa convolucional adecuada para Grad-CAM")

    def preprocess(self, image_bytes: bytes):
        # Convertir a escala de grises como en el entrenamiento
        image = Image.open(io.BytesIO(image_bytes)).convert("L")
        image = image.resize((224, 224))
        
        # Convertir a RGB artificial (1 canal -> 3 canales)
        rgb_image = Image.new("RGB", image.size)
        rgb_image.paste(image)
        
        # Preprocesamiento específico para DenseNet
        arr = np.array(rgb_image, dtype=np.float32)
        arr = preprocess_input(arr)
        arr = np.expand_dims(arr, axis=0)
        return arr, image

    def predict(self, image_bytes: bytes):
        arr, _ = self.preprocess(image_bytes)
        preds = self.model.predict(arr)
        return preds.tolist()
    
    def make_gradcam_heatmap(self, img_array, model, last_conv_layer_name, pred_index=None):
        # Crear un modelo que mapee la imagen de entrada a las activaciones
        # de la última capa convolucional y las predicciones de salida
        grad_model = Model(
            inputs=model.inputs,
            outputs=[model.get_layer(last_conv_layer_name).output, model.output]
        )

        # Calcular el gradiente para la clase superior predicha
        with tf.GradientTape() as tape:
            conv_outputs, predictions = grad_model(img_array)
            if pred_index is None:
                pred_index = tf.argmax(predictions[0])
            loss = predictions[:, pred_index]

        # Calcular gradientes
        grads = tape.gradient(loss, conv_outputs)
        
        # Vector de importancia de los filtros
        pooled_grads = tf.reduce_mean(grads, axis=(0, 1, 2))
        
        # Multiplicar cada canal en el mapa de características por su importancia
        conv_outputs = conv_outputs[0]
        heatmap = conv_outputs @ pooled_grads[..., tf.newaxis]
        heatmap = tf.squeeze(heatmap)
        
        # Normalizar el heatmap
        heatmap = tf.maximum(heatmap, 0) / tf.math.reduce_max(heatmap)
        return heatmap.numpy()

    def get_prediction_with_heatmap(self, image_bytes: bytes):
        arr, original_img = self.preprocess(image_bytes)
        preds = self.model.predict(arr)
        pred_class = np.argmax(preds[0])
        
        # Generar heatmap usando Grad-CAM
        heatmap = self.make_gradcam_heatmap(
            arr, 
            self.model, 
            self.last_conv_layer_name,
            pred_class
        )
        
        # Redimensionar y convertir heatmap
        heatmap = np.uint8(255 * heatmap)
        heatmap = Image.fromarray(heatmap).resize(original_img.size)
        heatmap = np.array(heatmap)
        
        # Aplicar colormap
        jet = cm.get_cmap("jet")
        heatmap_colored = jet(np.uint8(heatmap))[..., :3]
        heatmap_colored = np.uint8(heatmap_colored * 255)
        
        # Superponer con la imagen original
        original_img_rgb = original_img.convert("RGB")
        original_array = np.array(original_img_rgb)
        
        # Mezclar las imágenes
        alpha = 0.5
        overlay = (alpha * original_array + (1 - alpha) * heatmap_colored).astype(np.uint8)
        overlay_img = Image.fromarray(overlay)
        
        # Convertir a base64
        buffered = io.BytesIO()
        overlay_img.save(buffered, format="PNG")
        encoded_image = base64.b64encode(buffered.getvalue()).decode("utf-8")
        
        return {
            "predicted_class": self.class_names[pred_class],
            "probabilities": {
                self.class_names[0]: float(preds[0][0]),
                self.class_names[1]: float(preds[0][1]),
                self.class_names[2]: float(preds[0][2]),
            },
            "heatmap": encoded_image
        }
    
    def change_model(self, model_path: str):
        self.model_path = model_path
        self.model = self._load_model(model_path)
        self.last_conv_layer_name = self._find_last_conv_layer()