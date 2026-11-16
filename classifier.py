"""Classification service interface for the trained model and UI preview.

The UI talks only to the ``Classifier`` protocol defined here. Model mode loads
the local trained Keras model; demo mode exists only to preview the interface.

``DemoClassifier`` exists ONLY to preview the results layout. Its output is
derived from a hash of the image bytes — it does not look at the picture, it is
not AI, and the UI always labels it as demo data.
"""

from __future__ import annotations

import hashlib
import io
import logging
import os
import time
from dataclasses import dataclass
from functools import lru_cache
from typing import Protocol

import numpy as np
from PIL import Image, ImageOps

from .config import CLASS_LABELS, CLASS_NAMES_PATH, MODE_DEMO, MODE_MODEL, MODEL_PATH

logger = logging.getLogger(__name__)


class ClassifierUnavailableError(RuntimeError):
    """Raised when no usable classifier is available. Message is user-safe."""


@dataclass(frozen=True)
class ClassificationResult:
    image_id: str
    scores: dict[str, float]  # one score per label in CLASS_LABELS
    is_demo: bool

    def ranked(self) -> list[tuple[str, float]]:
        """All classes sorted from highest to lowest score (ties keep label order)."""
        order = {label: i for i, label in enumerate(CLASS_LABELS)}
        return sorted(self.scores.items(), key=lambda kv: (-kv[1], order.get(kv[0], 99)))

    @property
    def predicted(self) -> str:
        return self.ranked()[0][0]

    @property
    def confidence(self) -> float:
        """The model's score for the top class on THIS image (0–1).

        This is not the model's overall accuracy, which is measured separately
        on a test set.
        """
        return self.ranked()[0][1]


class Classifier(Protocol):
    name: str
    is_demo: bool

    def classify(self, image_id: str, image_bytes: bytes) -> ClassificationResult:
        """Classify one image. Must return a result carrying the same image_id."""
        ...


class DemoClassifier:
    """UI-preview stand-in. NOT a model and NOT a prediction."""

    name = "Demo (sample data)"
    is_demo = True

    def __init__(self, delay_seconds: float = 0.4) -> None:
        # Small delay so the loading/progress state is visible when previewing.
        self.delay_seconds = delay_seconds

    def classify(self, image_id: str, image_bytes: bytes) -> ClassificationResult:
        if self.delay_seconds:
            time.sleep(self.delay_seconds)
        digest = hashlib.sha256(image_bytes).digest()
        raw = [digest[i] + 1 for i in range(len(CLASS_LABELS))]
        raw[digest[len(CLASS_LABELS)] % len(CLASS_LABELS)] *= 4
        total = sum(raw)
        scores = {label: raw[i] / total for i, label in enumerate(CLASS_LABELS)}
        return ClassificationResult(image_id=image_id, scores=scores, is_demo=True)


class TrainedModelClassifier:
    """Run the trained Keras MobileNetV2 model for one image."""

    name = "Trained model"
    is_demo = False

    def __init__(self) -> None:
        self._model = _load_model()
        self._class_labels = _load_class_labels()
        if tuple(self._class_labels) != CLASS_LABELS:
            raise ClassifierUnavailableError(
                "The model class order does not match the WasteWise class mapping."
            )

    def classify(self, image_id: str, image_bytes: bytes) -> ClassificationResult:
        try:
            with Image.open(io.BytesIO(image_bytes)) as image:
                image = ImageOps.exif_transpose(image).convert("RGB").resize((224, 224))
            # Training fed MobileNetV2 images scaled to 0..1; the model's
            # embedded Rescaling(2, -1) layer then converts them to -1..1.
            batch = np.asarray(image, dtype=np.float32)[None, ...] / 255.0
            probabilities = np.asarray(self._model.predict(batch, verbose=0))[0]
        except Exception as exc:
            raise ClassifierUnavailableError(
                "The classification model could not process this image."
            ) from exc
        if probabilities.shape != (len(CLASS_LABELS),):
            raise ClassifierUnavailableError("The classification model returned an invalid output.")
        scores = {label: float(probabilities[i]) for i, label in enumerate(CLASS_LABELS)}
        return ClassificationResult(image_id=image_id, scores=scores, is_demo=False)


@lru_cache(maxsize=1)
def _load_model():
    if not MODEL_PATH.is_file():
        raise ClassifierUnavailableError("The trained classification model is missing.")
    try:
        os.environ.setdefault("KERAS_BACKEND", "torch")
        import keras
        # Models saved by newer Keras releases include this Dense config field.
        # On older Keras releases it is not a recognized constructor argument.
        # A null value carries no quantization settings, so strip only that
        # harmless field while loading; non-null settings still fail visibly.
        dense_init = keras.layers.Dense.__init__

        def compatible_dense_init(layer, *args, **kwargs):
            if kwargs.get("quantization_config", object()) is None:
                kwargs.pop("quantization_config")
            return dense_init(layer, *args, **kwargs)

        keras.layers.Dense.__init__ = compatible_dense_init
        try:
            return keras.models.load_model(MODEL_PATH, compile=False)
        finally:
            keras.layers.Dense.__init__ = dense_init
    except Exception as exc:
        logger.exception("Could not load the trained WasteWise model")
        raise ClassifierUnavailableError(
            "The trained model couldn’t start. Check that its file and required packages are installed."
        ) from exc


@lru_cache(maxsize=1)
def _load_class_labels() -> tuple[str, ...]:
    if not CLASS_NAMES_PATH.is_file():
        raise ClassifierUnavailableError("The model class-name file is missing.")
    labels = tuple(line.strip() for line in CLASS_NAMES_PATH.read_text(encoding="utf-8").splitlines() if line.strip())
    if len(labels) != len(CLASS_LABELS):
        raise ClassifierUnavailableError("The model class-name file is invalid.")
    return labels


def get_classifier(mode: str) -> Classifier:
    if mode == MODE_DEMO:
        return DemoClassifier()
    if mode == MODE_MODEL:
        return TrainedModelClassifier()
    raise ClassifierUnavailableError(f"Unknown classifier mode “{mode}”.")
