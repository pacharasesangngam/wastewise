"""Native Streamlit camera capture for the upload panel."""

from __future__ import annotations

import streamlit as st

from ..session import WasteWiseSession


def render(session: WasteWiseSession) -> None:
    """Capture an image with Streamlit's browser camera widget."""
    photo = st.camera_input(
        "Take a photo",
        key=f"camera_{session.uploader_nonce}",
        help="Allow camera access in your browser, then capture the item.",
    )
    if photo is None:
        return

    image_data = photo.getvalue()
    session.add_files([(f"webcam-{session.uploader_nonce + 1}.jpg", image_data)])
    # A fresh key clears the camera widget so the next capture can be added too.
    session.uploader_nonce += 1
