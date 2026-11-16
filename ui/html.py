"""Pure HTML builders for the UI (no Streamlit imports, so they are testable).

All output is single-line HTML with no blank lines or indentation, because
Streamlit's markdown renderer would otherwise treat indented lines as code.
All user-controlled text is escaped.
"""

from __future__ import annotations

from html import escape

from ..classifier import ClassificationResult
from ..config import APP_NAME, MAX_IMAGES
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
    mode_badge = (
        f'<div class="ww-chip ww-chip-demo">{icons.svg("flask-conical", 14)}'
        "<span>Sample mode</span></div>"
        if demo
        else '<div class="ww-chip ww-chip-live"><span class="ww-live-dot"></span><span>Trained model</span></div>'
    )
    return _flat(
        f"""
        <div class="ww-page-head">
          <div class="ww-header">
            <div class="ww-brand">
              <div class="ww-logo">{icons.svg("recycle", 23, "#FFFFFF")}</div>
              <div class="ww-brand-name">{escape(APP_NAME)}</div>
            </div>
            {mode_badge}
          </div>
        </div>
        """
    )


def hero_html() -> str:
    return '<div class="ww-hero"><div><h1>Give each item<br/>the right next stop.</h1><p>Add a photo to see what it is, which bin to use, and how to prepare it.<span class="ww-hero-th">ถ่ายรูปขยะเพื่อดูประเภท ถังที่ใช้ และวิธีเตรียมก่อนทิ้ง</span></p></div></div>'


def count_html(n: int) -> str:
    return f'<div class="ww-count">{n} / {MAX_IMAGES} images</div>'


def results_brand_html(demo: bool) -> str:
    label = "Sample mode" if demo else "Trained model"
    return f'<div class="ww-brand"><div class="ww-logo">{icons.svg("recycle",23,"#FFFFFF")}</div><div class="ww-brand-name">{escape(APP_NAME)}</div><span class="ww-results-model">{label}</span></div>'


def results_title_html(count: int) -> str:
    return f'<div class="ww-results-title"><h1><span class="ww-title-desktop">Sorted. Here is where each item goes.</span><span class="ww-title-mobile">Sorted. Here is where each goes.</span></h1><p><span class="ww-count-desktop">{count} items found · แยกประเภทได้ {count} ชิ้น</span><span class="ww-count-mobile">{count} items · แยกได้ {count} ชิ้น</span></p></div>'


def camera_brand_html() -> str:
    return f'<div class="ww-brand ww-camera-brand"><div class="ww-logo">{icons.svg("recycle",23,"#F2C230")}</div><div class="ww-brand-name">{escape(APP_NAME)}</div></div>'


def result_summary_html(result: ClassificationResult) -> str:
    g = get_guidance(result.predicted)
    tips = {
        "cardboard": (("Flatten the box", "พับกล่องให้แบน"), ("Remove tape and food residue", "แกะเทปและเศษอาหารออกถ้าทำได้"), ("Keep it dry", "เก็บให้แห้ง")),
        "glass": (("Empty and rinse", "เทของเหลวออกและล้างให้สะอาด"), ("Wrap broken glass safely", "ห่อเศษแก้วแตกให้มิดชิดก่อนทิ้ง")),
        "metal": (("Empty and rinse cans and tins", "เทของเหลวออกและล้างกระป๋อง"), ("Flatten if it is safe", "บีบให้แบนถ้าปลอดภัย")),
        "paper": (("Keep it clean and dry", "เก็บให้สะอาดและแห้ง"), ("Greasy paper may not be accepted", "กระดาษเปื้อนน้ำมันมากอาจรีไซเคิลไม่ได้")),
        "plastic": (("Empty, rinse and dry", "เทของเหลวออก ล้างและผึ่งให้แห้ง"), ("Check accepted plastic types locally", "ตรวจสอบประเภทพลาสติกที่รับในพื้นที่")),
        "trash": (("Use for items that cannot be recycled", "ใช้กับสิ่งของที่รีไซเคิลไม่ได้"), ("Check for special collection rules", "ตรวจสอบกฎการเก็บแยกเป็นพิเศษ")),
    }
    li = "".join(f'<li><span>{escape(en)}</span><small>{escape(th)}</small></li>' for en, th in tips[result.predicted])
    return _flat(f'''<div class="ww-result-summary"><h2>{escape(g.name_en)}<span>{escape(g.name_th)}</span></h2><ul class="ww-prep-list">{li}</ul></div>''')


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
    title = f"{selected} photo{'s' if selected != 1 else ''} ready" if selected else "Add a photo to begin"
    sub = (
        "Select Identify waste to see the material and bin guide for each photo."
        if selected
        else "Choose a photo or open the camera. We’ll show its material and where it goes."
    )
    tiles = "".join(
        f'<div class="ww-material-tile ww-material-{label}" style="--material:{get_guidance(label).accent}">'
        f'<span class="ww-material-tile-icon">{icons.svg(get_guidance(label).material_icon, 18)}</span>'
        f'<span><b>{escape(get_guidance(label).name_en)}</b><small>{escape(get_guidance(label).name_th)}</small></span>'
        "</div>"
        for label in ("cardboard", "glass", "metal", "paper", "plastic", "trash")
    )
    return _flat(
        f"""
        <div class="ww-empty-state">
          <div class="ww-empty-copy">
            <div class="ww-state-icon">{icons.svg("image", 25)}</div>
            <div class="ww-state-title">{escape(title)}</div>
          <div class="ww-state-sub">{escape(sub)}</div>
          </div>
          <div class="ww-material-key">{tiles}</div>
        </div>
        """
    )


def error_state_html(message: str) -> str:
    return _flat(
        f"""
        <div class="ww-state ww-state-error">
          <div class="ww-state-icon">{icons.svg("alert-circle", 28)}</div>
          <div class="ww-state-title">We couldn’t identify these items</div>
          <div class="ww-state-sub">{escape(message)}</div>
          <div class="ww-state-sub">Your photos are still here. Choose Identify waste to try again.</div>
        </div>
        """
    )


def result_html(result: ClassificationResult) -> str:
    g = get_guidance(result.predicted)
    demo = result.is_demo
    conf_label = "Sample confidence (demo)" if demo else "Model confidence"
    badge = (
        f'<div class="ww-chip ww-chip-demo">{icons.svg("flask-conical", 14)}'
        f"<span><b>{DEMO_LABEL}</b></span></div>"
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
