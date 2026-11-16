"""Constants and runtime configuration for WasteWise."""

from __future__ import annotations

import os
from pathlib import Path

APP_NAME = "WasteWise"
TAGLINE = "Let’s sort waste better!"

# Upload limits (enforced in the session logic, not only in the widget).
MAX_IMAGES = 5
MAX_FILE_MB = 200
MAX_FILE_BYTES = MAX_FILE_MB * 1024 * 1024
ALLOWED_EXTENSIONS = ("jpg", "jpeg", "png")

# The trained classifier predicts these six classes. Order is used as a tie-break.
CLASS_LABELS = ("cardboard", "glass", "metal", "paper", "plastic", "trash")

# Brand palette.
FOREST_GREEN = "#356B55"
SAGE_MIST = "#E4ECE5"
WARM_CREAM = "#F5F7F2"
DEEP_GREEN = "#20362D"

MODE_DEMO = "demo"
MODE_MODEL = "model"
MODEL_DIR = Path(
    os.environ.get("WASTEWISE_MODEL_DIR", Path(__file__).resolve().parent / "models")
).expanduser()
MODEL_PATH = MODEL_DIR / "trashnet_selected_model.keras"
CLASS_NAMES_PATH = MODEL_DIR / "class_names.txt"


def classifier_mode() -> str:
    """Which classifier the Classify Waste button should use.

    ``demo`` – UI-only sample data, always labelled as demo.
    ``model`` – the trained model shipped in ``models/``.

    Set with the ``WASTEWISE_MODE`` environment variable.
    """
    return os.environ.get("WASTEWISE_MODE", MODE_MODEL).strip().lower()
