import io
import pytest
import numpy as np
from unittest.mock import MagicMock, patch
from PIL import Image
from app.classifier import ImageClassifier


@pytest.fixture
def dummy_model():
    model = MagicMock()
    model.layers = [
        MagicMock(name="conv1", spec=["name"]),
        MagicMock(name="conv2", spec=["name"]),
    ]
    model.predict.return_value = np.array([[0.1, 0.8, 0.1]])  
    model.get_layer.return_value.output = np.random.rand(7, 7, 3)
    model.input = np.random.rand(1, 224, 224, 3)
    return model


@pytest.fixture
def classifier(dummy_model):
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
