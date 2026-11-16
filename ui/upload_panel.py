"""Left panel: image upload, previews and removal, and the Classify Waste button."""

from __future__ import annotations

import streamlit as st

from ..config import ALLOWED_EXTENSIONS
from ..session import STATUS_DONE, WasteWiseSession
from . import browser_camera
from . import html


def _on_upload(session: WasteWiseSession) -> None:
    """Move newly uploaded files into the session, then reset the widget.

    The session's list (with stable IDs) is the single source of truth. The
    uploader is only an "add files" control, so removing an image never leaves
    a stale file inside the widget.
    """
    key = f"uploader_{session.uploader_nonce}"
    files = st.session_state.get(key) or []
    session.add_files((f.name, f.getvalue()) for f in files)
    session.uploader_nonce += 1  # fresh, empty uploader on the next run


def _on_reset(session: WasteWiseSession) -> None:
    session.reset()


def _dismiss_notices(session: WasteWiseSession) -> None:
    session.clear_notices()


def render(session: WasteWiseSession) -> bool:
    """Draw the panel. Returns True when Classify Waste was clicked."""
    if session.notices:
        with st.container(key="notice_bar"):
            notice_col, close_col = st.columns([20, 1], gap="small")
            with notice_col:
                st.markdown(html.notices_html(session.notices), unsafe_allow_html=True)
            with close_col:
                st.button(
                    "",
                    key="dismiss_notices",
                    help="Dismiss notice",
                    icon=":material/close:",
                    on_click=_dismiss_notices,
                    args=(session,),
                )

    area_key = "upload_area_grid" if session.images else "upload_area_empty"
    with st.container(key=area_key, border=bool(session.images)):
        if session.images:
            st.markdown(html.count_html(len(session.images)), unsafe_allow_html=True)
            tiles = list(session.images)
            if not session.is_full:
                tiles.append(None)
            for start in range(0, len(tiles), 3):
                cols = st.columns(3, gap="small")
                for col, img in zip(cols, tiles[start : start + 3]):
                    with col:
                        if img is None:
                            with st.container(key="add_image_tile"):
                                st.file_uploader(
                                    "Add image",
                                    type=list(ALLOWED_EXTENSIONS),
                                    accept_multiple_files=True,
                                    key=f"uploader_{session.uploader_nonce}",
                                    on_change=_on_upload,
                                    args=(session,),
                                    label_visibility="collapsed",
                                )
                        else:
                            with st.container(key=f"thumb_card_{img.id}"):
                                st.markdown(html.thumb_html(img), unsafe_allow_html=True)
                                st.button(
                                    "",
                                    key=f"rm_{img.id}",
                                    help=f"Remove {img.name}",
                                    icon=":material/close:",
                                    on_click=session.remove,
                                    args=(img.id,),
                                )
        else:
            st.file_uploader(
                "Upload images",
                type=list(ALLOWED_EXTENSIONS),
                accept_multiple_files=True,
                key=f"uploader_{session.uploader_nonce}",
                on_change=_on_upload,
                args=(session,),
                label_visibility="collapsed",
            )

    if not session.is_full:
        with st.expander("Use webcam", expanded=False):
            browser_camera.render(session)

    completed = session.status == STATUS_DONE
    return st.button(
        "Start Over" if completed else "Classify Waste",
        key="classify_btn",
        type="secondary" if completed else "primary",
        icon=":material/refresh:" if completed else None,
        disabled=not session.images,
        on_click=_on_reset if completed else None,
        args=(session,) if completed else (),
    )
