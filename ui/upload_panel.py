"""Left panel: image upload, previews and removal, and the Classify Waste button."""

from __future__ import annotations

import streamlit as st

from ..config import ALLOWED_EXTENSIONS
from ..session import WasteWiseSession
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


def _toggle_webcam() -> None:
    st.session_state["webcam_open"] = not st.session_state.get("webcam_open", False)


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

    with st.container(key="upload_dock"):
        st.markdown(f'<div class="ww-dock-header"><div class="ww-dock-heading">Add photos</div><div class="ww-dock-sub">Up to 5 · เลือกได้ไม่เกิน 5 รูป</div></div>', unsafe_allow_html=True)
        area_key = "upload_area_grid" if session.images else "upload_area_empty"
        with st.container(key=area_key, border=bool(session.images)):
            if session.images:
                st.markdown(html.count_html(len(session.images)), unsafe_allow_html=True)
                tiles = list(session.images)
                if not session.is_full:
                    tiles.append(None)
                for start in range(0, len(tiles), 3):
                    row_tiles = tiles[start : start + 3]
                    cols = st.columns(len(row_tiles), gap="small")
                    for col, img in zip(cols, row_tiles):
                        with col:
                            if img is None:
                                with st.container(key="add_image_tile"):
                                    st.file_uploader("Add image", type=list(ALLOWED_EXTENSIONS), accept_multiple_files=True,
                                        key=f"uploader_{session.uploader_nonce}", on_change=_on_upload, args=(session,), label_visibility="collapsed")
                            else:
                                with st.container(key=f"thumb_card_{img.id}"):
                                    st.markdown(html.thumb_html(img), unsafe_allow_html=True)
                                    st.button("", key=f"rm_{img.id}", help=f"Remove {img.name}", icon=":material/close:", on_click=session.remove, args=(img.id,))
            else:
                st.file_uploader("Upload images", type=list(ALLOWED_EXTENSIONS), accept_multiple_files=True,
                    key=f"uploader_{session.uploader_nonce}", on_change=_on_upload, args=(session,), label_visibility="collapsed")

        if session.is_full:
            st.session_state["webcam_open"] = False
        action_camera, action_identify = st.columns(2, gap="small")
        with action_camera:
            if not session.is_full:
                st.button("Use webcam", key="webcam_toggle", icon=":material/videocam:", on_click=_toggle_webcam, use_container_width=True)
        with action_identify:
            run_requested = st.button("Identify waste", key="classify_btn", type="primary", use_container_width=True, disabled=not session.images)
        return run_requested


def render_camera(session: WasteWiseSession) -> bool:
    """Camera capture view with the native camera widget and photo queue."""
    head_brand, head_close = st.columns([3, 1], gap="small", vertical_alignment="center")
    with head_brand:
        st.markdown(html.camera_brand_html(), unsafe_allow_html=True)
    with head_close:
        st.button("×", key="camera_close", help="Close camera · ปิดกล้อง", on_click=lambda: setattr(st.session_state, "webcam_open", False), use_container_width=True)
    frame, queue = st.columns([3, 1], gap="large")
    with frame:
        with st.container(key="camera_frame"):
            st.markdown('<div class="ww-camera-live"><i></i>Live</div>', unsafe_allow_html=True)
            st.markdown('<div class="ww-camera-prompt"><strong>Place one item in the frame</strong><span>วางสิ่งของ 1 ชิ้นในกรอบ</span></div>', unsafe_allow_html=True)
            browser_camera.render(session)
    with queue:
        with st.container(key="camera_queue"):
            st.markdown(f'<div class="ww-captured-title"><strong>Captured</strong><span>{len(session.images)} of 5 · {len(session.images)} จาก 5</span></div>', unsafe_allow_html=True)
            if session.images:
                cols = st.columns(min(5, len(session.images)), gap="small")
                for col, img in zip(cols, session.images):
                    with col:
                        st.image(img.preview)
            st.markdown(f'<div class="ww-camera-count">{len(session.images)} of 5</div>', unsafe_allow_html=True)
            st.markdown('<div class="ww-camera-tip">Tip: good light and one item at a time work best.<br>เคล็ดลับ: แสงสว่างและวางทีละชิ้นจะแม่นยำที่สุด</div>', unsafe_allow_html=True)
            if session.images and st.button(f"Identify {len(session.images)} photo" if len(session.images) == 1 else f"Identify {len(session.images)} photos", key="camera_identify", type="primary", use_container_width=True):
                return True
            if st.button("Done", key="camera_done", use_container_width=True, on_click=lambda: setattr(st.session_state, "webcam_open", False)):
                return False
    return False
