"""Right panel: empty, loading, error and results (one tab per image) states."""

from __future__ import annotations

import streamlit as st

from .. import config
from ..classifier import get_classifier
from ..session import STATUS_DONE, STATUS_ERROR, WasteWiseSession
from ..guidance import get_guidance
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
    if session.status == STATUS_DONE:
        st.session_state.wastewise_view = "results"
    holder.empty()
    st.rerun()


def render_home(session: WasteWiseSession, run_requested: bool) -> None:
    if run_requested:
        _run_classification(session)

    if session.status == STATUS_ERROR:
        st.markdown(html.error_state_html(session.error or ""), unsafe_allow_html=True)
        return

    st.markdown('<div class="ww-home-support"><div><div class="ww-section-title">Sorting results</div><div class="ww-section-sub">Material, bin, and prep tips · ประเภทขยะ ถัง และวิธีเตรียม</div></div></div>', unsafe_allow_html=True)
    st.markdown(html.empty_state_html(len(session.images)), unsafe_allow_html=True)


def render_results(session: WasteWiseSession, demo: bool) -> None:
    entries = session.result_entries()
    nav_back, nav_brand = st.columns([1, 4], gap="small", vertical_alignment="center")
    with nav_back:
        st.button("←", key="new_photos", help="New photos · เพิ่มรูปใหม่", on_click=lambda: setattr(st.session_state, "wastewise_view", "upload"))
    with nav_brand:
        st.markdown(html.results_brand_html(demo), unsafe_allow_html=True)
    st.markdown(html.results_title_html(len(entries)), unsafe_allow_html=True)
    if session.status == STATUS_ERROR:
        st.markdown(html.error_state_html(session.error or ""), unsafe_allow_html=True)
        if st.button("Back to photos · กลับไปที่รูป", key="error_back"):
            st.session_state.wastewise_view = "upload"
            st.rerun()
        return
    main, side = st.columns([1.65, .8], gap="large")
    with main:
        for pos, image, result in entries:
            with st.container(key=f"result_card_{image.id}"):
                g = get_guidance(result.predicted)
                st.markdown(f'<div class="ww-bin-band" style="--material:{g.accent}">{g.name_en} bin · ถัง{g.name_th}</div>', unsafe_allow_html=True)
                photo, detail = st.columns([.72, 1.28], gap="medium")
                with photo:
                    st.image(image.preview)
                with detail:
                    st.markdown(html.result_summary_html(result), unsafe_allow_html=True)
                    with st.expander("Model scores · คะแนนจากโมเดล"):
                        st.markdown(html.scores_html(result), unsafe_allow_html=True)
    with side:
        with st.container(key="bins_summary"):
            st.markdown('<div class="ww-side-title">Your bins</div><div class="ww-side-th">สรุปถังที่ใช้</div>', unsafe_allow_html=True)
            counts = {}
            for _, _, result in entries:
                counts[result.predicted] = counts.get(result.predicted, 0) + 1
            for label, amount in counts.items():
                g = get_guidance(label)
                st.markdown(f'<div class="ww-bin-count"><span>{g.name_en} · {g.name_th}</span><b>{amount}</b></div>', unsafe_allow_html=True)
            st.button("Add more photos", key="add_more", type="primary", use_container_width=True, on_click=lambda: setattr(st.session_state, "wastewise_view", "upload"))
            if st.button("Start over", key="start_over", use_container_width=True):
                session.reset()
                st.session_state.wastewise_view = "upload"
                st.session_state.webcam_open = False
                st.rerun()
