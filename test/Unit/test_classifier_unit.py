import io
import pytest
import numpy as np
from unittest.mock import MagicMock, patch
from PIL import Image
from app.classifier import ImageClassifier
from tensorflow.keras.models import load_model, Model
from tensorflow.keras.preprocessing import image
import tensorflow as tf 

@pytest.fixture
def dummy_model():
    # Definir entradas funcionales
    inputs = tf.keras.Input(shape=(224, 224, 3), name="input_layer")

    # Una capa convolucional simulada
    x = tf.keras.layers.Conv2D(8, (3, 3), activation="relu", name="conv_layer")(inputs)
    x = tf.keras.layers.GlobalAveragePooling2D()(x)
    outputs = tf.keras.layers.Dense(3, activation="softmax", name="output_layer")(x)

    # Crear modelo funcional
    model = tf.keras.Model(inputs=inputs, outputs=outputs, name="dummy_model")
    return model


@pytest.fixture
def classifier(dummy_model):
    # Simular carga de modelo con patch
    with patch("app.classifier.load_model", return_value=dummy_model):
        return ImageClassifier("fake_model.h5", ["sano", "viral", "bacteriana"])

def generate_test_image():
    img = Image.new("RGB", (224, 224), color="white")
    buf = io.BytesIO()
    img.save(buf, format="PNG")
    return buf.getvalue()


# ------------------------------------------------
# TESTS
# ------------------------------------------------

def test_preprocess_image(classifier):
    img_bytes = generate_test_image()
    img_array, img = classifier.preprocess_image(img_bytes)
    assert img_array.shape == (1, 224, 224, 3)
    assert isinstance(img, Image.Image)

def test_predict(classifier):
    img_bytes = generate_test_image()
    result = classifier.predict(img_bytes)
    assert "predicted_class" in result
    assert "probabilities" in result
    assert result["predicted_class"] in classifier.class_names

def test_predict_heatmap(classifier):
    img_bytes = generate_test_image()
    result = classifier.predict_heatmap(img_bytes)
    assert "predicted_class" in result
    assert "heatmap" in result
    assert isinstance(result["heatmap"], str)  

def test_make_gradcam_heatmap(classifier, dummy_model):
    img_array = np.random.rand(1, 224, 224, 3)
    heatmap = classifier.make_gradcam_heatmap(img_array, 0)
    assert isinstance(heatmap, np.ndarray)
    assert heatmap.ndim == 2

def test_overlay_heatmap(classifier):
    img = Image.new("RGB", (224, 224), color="gray")
    heatmap = np.random.rand(224, 224)
    result_img = classifier.overlay_heatmap(heatmap, img)
    assert isinstance(result_img, Image.Image)
