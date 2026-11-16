"""Streamlit entry point for WasteWise."""

from __future__ import annotations

import streamlit as st

from wastewise import config
from wastewise.session import WasteWiseSession
from wastewise.ui import html, results_panel, theme, upload_panel


st.set_page_config(page_title=config.APP_NAME, page_icon="♻️", layout="wide")
st.markdown(theme.style_tag(), unsafe_allow_html=True)

if "wastewise_session" not in st.session_state:
    st.session_state.wastewise_session = WasteWiseSession()
session = st.session_state.wastewise_session
if "wastewise_view" not in st.session_state:
    st.session_state.wastewise_view = "upload"

if st.session_state.get("webcam_open", False) and not session.is_full:
    run_requested = upload_panel.render_camera(session)
    if run_requested:
        results_panel.render_home(session, True)
elif session.status == "done" and st.session_state.wastewise_view == "results":
    results_panel.render_results(session, config.classifier_mode() == config.MODE_DEMO)
else:
    st.markdown(html.header_html(config.classifier_mode() == config.MODE_DEMO), unsafe_allow_html=True)
    copy, intake = st.columns([1, 1], gap="large", vertical_alignment="center")
    with copy:
        st.markdown(html.hero_html(), unsafe_allow_html=True)
    with intake:
        with st.container(key="left_panel"):
            run_requested = upload_panel.render(session)
    results_panel.render_home(session, run_requested)
