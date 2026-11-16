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

st.markdown(html.header_html(config.classifier_mode() == config.MODE_DEMO), unsafe_allow_html=True)
left, right = st.columns([1, 1.05], gap="large")
with left:
    with st.container(key="left_panel"):
        st.markdown(
            '<div class="ww-section-head"><div class="ww-section-title">Add your items</div>'
            '<div class="ww-section-sub">Upload up to five clear photos to get started.</div></div>',
            unsafe_allow_html=True,
        )
        run_requested = upload_panel.render(session)
with right:
    with st.container(key="right_panel"):
        st.markdown(
            '<div class="ww-section-head"><div class="ww-section-title">Sorting guidance</div>'
            '<div class="ww-section-sub">A simple next step for every item.</div></div>',
            unsafe_allow_html=True,
        )
        results_panel.render(session, run_requested)
