"""A browser getUserMedia webcam control for Streamlit."""

from __future__ import annotations

import base64
from pathlib import Path

import streamlit as st
import streamlit.components.v1 as components

from ..session import WasteWiseSession

_camera = components.declare_component(
    "wastewise_browser_camera",
    path=str(Path(__file__).with_name("browser_camera")),
)


def render(session: WasteWiseSession) -> None:
    """Show a live browser webcam and add a captured JPEG to the session."""
    capture = _camera(key="wastewise_browser_camera", default=None, height=350)
    if not isinstance(capture, dict) or not capture.get("id"):
        return

    capture_id = str(capture["id"])
    if st.session_state.get("last_camera_capture_id") == capture_id:
        return
    st.session_state.last_camera_capture_id = capture_id

    try:
        data_url = capture["data"]
        encoded = data_url.split(",", 1)[1]
        image_data = base64.b64decode(encoded, validate=True)
    except (KeyError, IndexError, ValueError, TypeError):
        session.notices = ["The webcam photo could not be read. Please try again."]
        return

    session.add_files([(f"webcam-{capture_id[:8]}.jpg", image_data)])
