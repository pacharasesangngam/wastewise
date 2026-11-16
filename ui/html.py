"""Pure HTML builders for the UI (no Streamlit imports, so they are testable).

All output is single-line HTML with no blank lines or indentation, because
Streamlit's markdown renderer would otherwise treat indented lines as code.
All user-controlled text is escaped.
"""

from __future__ import annotations

from html import escape

from ..classifier import ClassificationResult
from ..config import APP_NAME, MAX_IMAGES, TAGLINE
from ..guidance import get_guidance
from ..images import SelectedImage
from . import icons

DEMO_LABEL = "Demo mode"
DEMO_DETAIL = "Sample results for previewing the layout — not a trained model."


def _flat(s: str) -> str:
    return "".join(line.strip() for line in s.splitlines())


def pct(value: float) -> str:
    return f"{value * 100:.1f}%"


def header_html(demo: bool) -> str:
    return _flat(
        f"""
        <div class="ww-header">
          <div class="ww-logo">{icons.svg("recycle", 24, "#FFFFFF")}</div>
          <div class="ww-brand">
            <div class="ww-title">{escape(APP_NAME)}</div>
            <div class="ww-tagline">{escape(TAGLINE)}</div>
          </div>
          <div class="ww-spacer"></div>
        </div>
        """
    )


def count_html(n: int) -> str:
    return f'<div class="ww-count">{n} / {MAX_IMAGES} images</div>'


def thumb_html(image: SelectedImage) -> str:
    return _flat(
        f"""
        <div class="ww-thumb" title="{escape(image.name)}">
          <img alt="{escape(image.name)}" src="data:image/jpeg;base64,{image.thumb_b64}"/>
          <div class="ww-thumb-name">{escape(image.name)}</div>
        </div>
        """
    )


def notices_html(notices: list[str]) -> str:
    if not notices:
        return ""
    items = "".join(
        f'<div class="ww-notice">{icons.svg("alert-circle", 16)}<span>{escape(n)}</span></div>'
        for n in notices
    )
    return f'<div class="ww-notices">{items}</div>'


def empty_state_html(selected: int) -> str:
    sub = (
        f"{selected} image{'s' if selected != 1 else ''} selected. "
        "Results will appear here after classification."
        if selected
        else "Upload images to get started."
    )
    return _flat(
        f"""
        <div class="ww-state">
          <div class="ww-state-icon">{icons.svg("image", 28)}</div>
          <div class="ww-state-title">No results yet</div>
          <div class="ww-state-sub">{escape(sub)}</div>
        </div>
        """
    )


def error_state_html(message: str) -> str:
    return _flat(
        f"""
        <div class="ww-state ww-state-error">
          <div class="ww-state-icon">{icons.svg("alert-circle", 28)}</div>
          <div class="ww-state-title">We couldn’t classify your images</div>
          <div class="ww-state-sub">{escape(message)}</div>
          <div class="ww-state-sub">Your selected images are still here. You can try again.</div>
        </div>
        """
    )


def result_html(result: ClassificationResult) -> str:
    g = get_guidance(result.predicted)
    demo = result.is_demo
    conf_label = "Sample confidence (demo)" if demo else "Model confidence"
    badge = (
        f'<div class="ww-chip ww-chip-demo">{icons.svg("flask-conical", 14)}'
        f"<span><b>{DEMO_LABEL}</b> · sample data</span></div>"
        if demo
        else ""
    )
    return _flat(
        f"""
        <div class="ww-result">
          {badge}
          <div class="ww-kicker">Predicted material</div>
          <div class="ww-material">
            <span class="ww-material-icon">{icons.svg(g.material_icon, 22)}</span>
            <span class="ww-material-en">{escape(g.name_en)}</span>
            <span class="ww-material-th">{escape(g.name_th)}</span>
          </div>
          <div class="ww-conf">
            <div class="ww-conf-row"><span>{conf_label}</span><b>{pct(result.confidence)}</b></div>
            <div class="ww-bar"><div class="ww-bar-fill" style="width:{result.confidence * 100:.1f}%"></div></div>
            <div class="ww-fine">Confidence for this image only — not the model’s overall accuracy.</div>
          </div>
          <div class="ww-bin" style="--accent:{g.accent}">
            <div class="ww-bin-icon">{icons.svg(g.bin_icon, 30, "#FFFFFF")}</div>
            <div>
              <div class="ww-kicker ww-kicker-light">Recommended bin</div>
              <div class="ww-bin-name">{escape(g.bin_en)}</div>
              <div class="ww-bin-th">{escape(g.bin_th)}</div>
            </div>
          </div>
          <div class="ww-instr">
            <div>{escape(g.instructions_en)}</div>
            <div class="ww-instr-th">{escape(g.instructions_th)}</div>
          </div>
          <div class="ww-fine">Bin names and colors vary by location — follow local signage and rules.</div>
        </div>
        """
    )


def scores_html(result: ClassificationResult) -> str:
    top = result.predicted
    rows = []
    for label, score in result.ranked():
        g = get_guidance(label)
        is_top = label == top
        check = f'<span class="ww-score-check">{icons.svg("check", 14)}</span>' if is_top else ""
        rows.append(
            f'<div class="ww-score{" is-top" if is_top else ""}">'
            f'<div class="ww-score-name">{check}{escape(g.name_en)}'
            f' <span class="ww-score-th">{escape(g.name_th)}</span></div>'
            f'<div class="ww-bar"><div class="ww-bar-fill" style="width:{score * 100:.1f}%"></div></div>'
            f'<div class="ww-score-val">{pct(score)}</div></div>'
        )
    return f'<div class="ww-scores">{"".join(rows)}</div>'
