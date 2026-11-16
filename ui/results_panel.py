"""Right panel: empty, loading, error and results (one tab per image) states."""

from __future__ import annotations

import streamlit as st

from .. import config
from ..classifier import get_classifier
from ..session import STATUS_DONE, STATUS_ERROR, WasteWiseSession
from . import html


def _run_classification(session: WasteWiseSession) -> None:
    st.session_state["webcam_open"] = False
    holder = st.empty()
    with holder.container():
        bar = st.progress(0.0, text="Getting your results ready…")

        def on_progress(done: int, total: int) -> None:
            if done < total:
                bar.progress(done / total, text=f"Classifying image {done + 1} of {total}…")
            else:
                bar.progress(1.0, text="All items identified")

        session.classify(lambda: get_classifier(config.classifier_mode()), on_progress)
    holder.empty()
    st.rerun()


def _render_entry(image, result) -> None:
    left, right = st.columns([4, 6], gap="medium")
    with left:
        st.image(image.preview, caption=image.name)
    with right:
        st.markdown(html.result_html(result), unsafe_allow_html=True)
        with st.expander("All class scores"):
            st.markdown(html.scores_html(result), unsafe_allow_html=True)


def render(session: WasteWiseSession, run_requested: bool) -> None:
    if run_requested:
        _run_classification(session)

    if session.status == STATUS_ERROR:
        st.markdown(html.error_state_html(session.error or ""), unsafe_allow_html=True)
        return

    entries = session.result_entries() if session.status == STATUS_DONE else []
    if not entries:
        st.markdown(html.empty_state_html(len(session.images)), unsafe_allow_html=True)
        return

    tabs = st.tabs([f"Item {pos + 1}" for pos, _, _ in entries])
    for tab, (_, image, result) in zip(tabs, entries):
        with tab:
            _render_entry(image, result)
