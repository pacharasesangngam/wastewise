"""Native Streamlit camera capture for the upload panel."""

from __future__ import annotations

import streamlit as st

from ..session import WasteWiseSession


def render(session: WasteWiseSession) -> None:
    """Capture an image with Streamlit's browser camera widget."""
    # Keep this widget key stable. Replacing it immediately after a capture
    # remounts Streamlit's camera input and makes mobile browsers jump to the
    # top of the page.
    photo = st.camera_input(
        "Take a photo",
        key="camera_capture",
        help="Allow camera access in your browser, then capture the item.",
    )
    if photo is None:
        st.session_state["camera_photo_processed"] = False
        return

    # Streamlit reruns the script while retaining the captured file in the
    # widget. Only add it once; its built-in Clear photo control returns to the
    # live preview without remounting the widget.
    if not st.session_state.get("camera_photo_processed", False):
        image_data = photo.getvalue()
        session.add_files([(f"webcam-{len(session.images) + 1}.jpg", image_data)])
        st.session_state["camera_photo_processed"] = True
        # Return to WasteWise's own photo grid instead of leaving the large
        # native Streamlit snapshot preview on screen. Users can reopen the
        # camera to add another image.
        st.session_state["webcam_open"] = False
        st.rerun()
