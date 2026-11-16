"""Page styling: palette, Prompt font, and layout CSS (pure — returns strings)."""

from __future__ import annotations

import re
from urllib.parse import quote

from ..config import (
    DEEP_GREEN,
    FOREST_GREEN,
    MAX_FILE_MB,
    MAX_IMAGES,
    SAGE_MIST,
    WARM_CREAM,
)

FONT_IMPORT = (
    "@import url('https://fonts.googleapis.com/css2?"
    "family=Prompt:wght@300;400;500;600;700&display=swap');"
)

# The single upload area shows a "+" badge; it is drawn here so the page has
# only ONE upload control (the real st.file_uploader dropzone).
_PLUS_SVG = (
    "<svg xmlns='http://www.w3.org/2000/svg' width='40' height='40' viewBox='0 0 40 40'>"
    f"<circle cx='20' cy='20' r='20' fill='{FOREST_GREEN}'/>"
    "<path d='M12 20h16M20 12v16' stroke='white' stroke-width='2.5' stroke-linecap='round'/></svg>"
)
PLUS_DATA_URI = "data:image/svg+xml;utf8," + quote(_PLUS_SVG, safe="")

_CSS = """
:root{
  --ww-green:__GREEN__; --ww-sage:__SAGE__; --ww-cream:__CREAM__; --ww-deep:__DEEP__;
  --ww-border:#D3E0CE; --ww-muted:#5E7266; --ww-radius:14px; --ww-amber:#D9A441;
}
html, body, .stApp, .stApp *:not([data-testid="stIconMaterial"]):not(svg):not(path){
  font-family:'Prompt',system-ui,-apple-system,'Segoe UI',sans-serif;
}
[data-testid="stIconMaterial"]{font-family:'Material Symbols Rounded','Material Symbols Outlined' !important;}
.stApp{background:var(--ww-cream); color:var(--ww-deep);}
header[data-testid="stHeader"], [data-testid="stToolbar"], [data-testid="stDecoration"], footer, #MainMenu{display:none !important;}
.block-container{padding:1.25rem 1.6rem 1.5rem !important; max-width:1440px;}

/* Header */
.ww-header{display:flex; align-items:center; gap:.85rem; padding:.2rem 0 1.1rem; margin-bottom:1.2rem; border-bottom:1px solid var(--ww-border);}
.ww-logo{width:46px; height:46px; border-radius:15px 15px 15px 5px; background:var(--ww-green); display:flex; align-items:center; justify-content:center; flex:none;}
.ww-title{font-size:1.45rem; font-weight:700; line-height:1.1; color:var(--ww-deep); letter-spacing:-.025em;}
.ww-tagline{font-size:.85rem; color:var(--ww-muted); margin-top:4px;}
.ww-spacer{flex:1;}
.ww-header-meta{display:flex; align-items:center; justify-content:flex-end; gap:.65rem;}
.ww-material-count{font-size:.8rem; color:var(--ww-muted); padding-right:.7rem; border-right:1px solid var(--ww-border);}
.ww-chip{display:inline-flex; align-items:center; gap:.4rem; padding:.3rem .65rem; border-radius:999px; font-size:.78rem; line-height:1.3;}
.ww-chip-demo{background:#FFF5DC; color:#654700; border:1px solid #E8CB83;}
.ww-chip svg{flex:none;}
.ww-section-head{margin:0 0 .85rem;}
.ww-section-title{font-size:1.08rem; font-weight:650; letter-spacing:-.015em; color:var(--ww-deep);}
.ww-section-sub{font-size:.8rem; color:var(--ww-muted); margin-top:.12rem;}

/* Panels */
.st-key-left_panel{gap:.8rem !important; padding:1rem 1.1rem 1.2rem; border:1px solid var(--ww-border); border-top:3px solid var(--ww-green); border-radius:4px 4px 16px 16px; background:#fff; min-height:calc(100vh - 9rem);}
.st-key-right_panel{padding:1rem 1.1rem 1.2rem; gap:1rem !important; border:1px solid var(--ww-border); border-top:3px solid #C8D9C7; border-radius:4px 4px 16px 16px; background:#fff; min-height:calc(100vh - 9rem);}

/* Upload area */
.st-key-upload_area_grid{padding:.8rem !important; border:2px dashed var(--ww-green) !important; border-radius:var(--ww-radius) !important; background:var(--ww-sage);}
.st-key-upload_area_grid > div:first-child{gap:.8rem;}
.st-key-upload_area_grid [data-testid="stHorizontalBlock"]{margin-bottom:.55rem;}
.st-key-upload_area_empty{padding:0 !important; border:0 !important; background:transparent !important;}
[data-testid="stFileUploader"] > label{display:none;}
[data-testid="stFileUploaderDropzone"]{
  position:relative; display:flex; flex-direction:column; align-items:center; justify-content:center; gap:.45rem;
  min-height:128px; padding:1rem; text-align:center;
  border:2px dashed var(--ww-green); border-radius:var(--ww-radius); background:var(--ww-sage);
  transition:background .15s ease, border-color .15s ease;
}
[data-testid="stFileUploaderDropzone"]:hover{background:#E3EEDD;}
[data-testid="stFileUploaderDropzone"]::before{
  content:""; display:block; flex:0 0 40px; width:40px; height:40px; margin:0 auto;
  background:url("__PLUS__") center/contain no-repeat;
}
[data-testid="stFileUploaderDropzoneInstructions"]{display:flex !important; flex-direction:column; align-items:center; gap:.1rem;}
[data-testid="stFileUploaderDropzoneInstructions"] > *{display:none !important;}
[data-testid="stFileUploaderDropzoneInstructions"]::before{content:"Upload up to __MAX__ images"; font-weight:600; font-size:1rem; color:var(--ww-deep);}
[data-testid="stFileUploaderDropzoneInstructions"]::after{content:"__LIMIT__MB per file (JPG, JPEG, PNG)"; font-size:.78rem; color:var(--ww-muted);}
[data-testid="stFileUploaderDropzone"] button{position:absolute; inset:0; width:100%; height:100%; opacity:0; cursor:pointer; z-index:2;}
[data-testid="stFileUploaderDropzone"]:has(button:disabled){opacity:.5; border-color:var(--ww-border); cursor:not-allowed;}
[data-testid="stFileUploaderDropzone"]:has(button:disabled) button{cursor:not-allowed;}
[data-testid="stFileUploaderFile"]{font-size:.8rem;}

.ww-count{font-size:.78rem; color:var(--ww-muted); font-weight:500; margin-top:.1rem;}
[class*="st-key-thumb_card_"]{position:relative; min-width:0; padding-bottom:.15rem;}
.ww-thumb{position:relative; border-radius:12px; overflow:hidden; border:1px solid var(--ww-border); background:#fff;}
.ww-thumb img{width:100%; aspect-ratio:1/1; object-fit:cover; display:block;}
.ww-thumb-name{padding:.25rem .4rem .35rem; overflow:hidden; text-overflow:ellipsis; white-space:nowrap; color:var(--ww-deep); font-size:.7rem;}
[class*="st-key-rm_"]{position:absolute; top:.35rem; right:.35rem; z-index:3;}
[class*="st-key-rm_"] button{min-height:1.45rem; width:1.45rem; padding:0; border-radius:999px; border:1px solid rgba(255,255,255,.9); background:rgba(38,58,45,.78); color:#fff; font-size:.65rem;}
[class*="st-key-rm_"] button:hover{border-color:#fff; background:var(--ww-green); color:#fff;}
.st-key-add_image_tile{position:relative; min-width:0; aspect-ratio:1/1; border:0; border-radius:12px; background:transparent; overflow:hidden;}
.st-key-add_image_tile [data-testid="stFileUploader"]{height:100%;}
.st-key-add_image_tile [data-testid="stFileUploaderDropzone"]{height:100%; min-height:0; padding:0; border:0; border-radius:0; background:transparent; align-items:center; justify-content:center;}
.st-key-add_image_tile [data-testid="stFileUploaderDropzone"]::before{width:38px; height:38px; flex-basis:38px;}
.st-key-add_image_tile [data-testid="stFileUploaderDropzoneInstructions"]{display:none !important;}
.st-key-add_image_tile [data-testid="stFileUploaderDropzone"] button{opacity:0;}
.st-key-upload_area_empty [data-testid="stFileUploaderDropzone"]{min-height:128px; padding:1rem;}
.st-key-upload_area_empty [data-testid="stFileUploaderDropzone"]::before{width:40px; height:40px; flex-basis:40px;}
.st-key-upload_area_empty [data-testid="stFileUploaderDropzoneInstructions"]::before{content:"Upload up to __MAX__ images"; font-size:1rem;}
.st-key-upload_area_empty [data-testid="stFileUploaderDropzoneInstructions"]::after{content:"__LIMIT__MB per file (JPG, JPEG, PNG)"; display:block; font-size:.78rem;}
.ww-notices{display:flex; flex-direction:column; gap:.35rem;}
.st-key-notice_bar{margin-bottom:1rem; padding:.55rem .8rem; border-radius:12px; background:#FFF3D6; border:1px solid #F0D79A;}
.st-key-notice_bar [data-testid="stHorizontalBlock"]{align-items:center; gap:0 !important;}
.st-key-notice_bar [data-testid="stColumn"]{padding:0 !important; min-height:0 !important;}
.st-key-notice_bar [data-testid="stMarkdown"],
.st-key-notice_bar [data-testid="stMarkdownContainer"],
.st-key-notice_bar [data-testid="stMarkdownContainer"] > div{margin:0 !important; padding:0 !important;}
.st-key-notice_bar .ww-notice{display:flex; gap:.45rem; align-items:center; min-height:1.8rem; padding:0; border:0; border-radius:0; font-size:.8rem; line-height:1.35; background:transparent; color:#6B4A00;} .ww-notice-text{ flex:1; min-width:0;}
.st-key-notice_bar .ww-notice svg{flex:none; margin:0;}
.st-key-notice_bar [class*="st-key-dismiss_notices"]{display:flex; align-items:center; justify-content:center; margin:0 !important; padding:0 !important;}
.st-key-notice_bar [class*="st-key-dismiss_notices"] button{display:flex; align-items:center; justify-content:center; min-height:1.8rem; height:1.8rem; width:1.8rem; margin:0; padding:0; border:0; border-radius:0; background:transparent; color:#6B4A00; box-shadow:none;}
.st-key-notice_bar [class*="st-key-dismiss_notices"] button:hover{border:0; background:transparent; color:#4F3700; box-shadow:none;}

/* Primary action */
.st-key-classify_btn{margin-top:.2rem;}
.st-key-classify_btn button{width:100%; min-height:3rem; border-radius:12px; border:none; background:var(--ww-green); color:#fff; font-size:1rem; font-weight:600; letter-spacing:.01em;}
.st-key-classify_btn button:hover:not(:disabled){background:#2F6747; color:#fff;}
.st-key-classify_btn button:disabled{background:var(--ww-green); opacity:.4; color:#fff;}
.st-key-classify_btn button:focus-visible,
[data-testid="stFileUploaderDropzone"] button:focus-visible,
[class*="st-key-rm_"] button:focus-visible,
[class*="st-key-dismiss_notices"] button:focus-visible{outline:3px solid var(--ww-amber) !important; outline-offset:3px;}

/* Results */
.ww-state{display:flex; flex-direction:column; align-items:center; text-align:center; gap:.35rem; padding:4.5rem 1rem; border:1px dashed var(--ww-border); border-radius:var(--ww-radius); background:linear-gradient(145deg,#F5F8F1,#FBFCF9);}
.ww-state-icon{width:56px; height:56px; border-radius:16px; background:var(--ww-sage); color:var(--ww-green); display:flex; align-items:center; justify-content:center; margin-bottom:.3rem;}
.ww-state-title{font-weight:600; font-size:1.05rem;}
.ww-state-sub{font-size:.88rem; color:var(--ww-muted); max-width:34rem;}
.ww-state-error{border-style:solid; border-color:#E8C4BC; background:#FDF1EE;}
.ww-state-error .ww-state-icon{background:#F8DDD7; color:#A5392B;}

.stTabs [data-baseweb="tab-list"]{gap:.25rem; border-bottom:1px solid var(--ww-border);}
.stTabs [data-baseweb="tab"]{height:2.4rem; padding:0 .9rem; font-weight:500; color:var(--ww-muted);}
.stTabs [aria-selected="true"]{color:var(--ww-green) !important; font-weight:600;}
.stTabs [data-baseweb="tab-highlight"]{background-color:var(--ww-green) !important;}
.stTabs [data-baseweb="tab-border"]{display:none;}

.ww-result{display:flex; flex-direction:column; gap:.75rem;}
.ww-result .ww-chip{align-self:flex-start;}
.ww-kicker{font-size:.72rem; font-weight:600; text-transform:uppercase; letter-spacing:.06em; color:var(--ww-muted);}
.ww-kicker-light{color:rgba(255,255,255,.8);}
.ww-material{display:flex; align-items:center; flex-wrap:wrap; gap:.55rem; margin-top:-.45rem;}
.ww-material-icon{width:40px; height:40px; border-radius:12px; background:var(--ww-sage); color:var(--ww-green); display:flex; align-items:center; justify-content:center;}
.ww-material-en{font-size:1.7rem; font-weight:700; line-height:1.1;}
.ww-material-th{font-size:1.15rem; color:var(--ww-muted); font-weight:500;}
.ww-conf-row{display:flex; justify-content:space-between; font-size:.88rem; margin-bottom:.3rem;}
.ww-conf-row b{color:var(--ww-green);}
.ww-bar{height:8px; border-radius:999px; background:var(--ww-sage); overflow:hidden;}
.ww-bar-fill{height:100%; border-radius:999px; background:var(--ww-green);}
.ww-fine{font-size:.74rem; color:var(--ww-muted); margin-top:.3rem;}
.ww-bin{display:flex; align-items:center; gap:.9rem; padding:.9rem 1.1rem; border-radius:var(--ww-radius); background:var(--accent,var(--ww-green)); color:#fff;}
.ww-bin-icon{width:52px; height:52px; border-radius:14px; background:rgba(255,255,255,.18); display:flex; align-items:center; justify-content:center; flex:none;}
.ww-bin-name{font-size:1.2rem; font-weight:700; line-height:1.2;}
.ww-bin-th{font-size:.9rem; opacity:.9;}
.ww-instr{font-size:.92rem; line-height:1.5;}
.ww-instr-th{color:var(--ww-muted); margin-top:.15rem;}

[data-testid="stExpander"] details{border:1px solid var(--ww-border) !important; border-radius:12px !important; background:#fff;}
[data-testid="stExpander"] summary{font-weight:500; font-size:.9rem;}
.ww-scores{display:flex; flex-direction:column; gap:.4rem;}
.ww-score{display:grid; grid-template-columns:minmax(170px,1.6fr) 2fr 3.6rem; align-items:center; gap:.7rem; padding:.3rem .5rem; border-radius:9px; font-size:.86rem;}
.ww-score.is-top{background:var(--ww-sage); font-weight:600;}
.ww-score-name{display:flex; align-items:center; flex-wrap:wrap; column-gap:.35rem;}
.ww-score-th{color:var(--ww-muted); font-weight:400; font-size:.8rem; white-space:nowrap;}
.ww-score-check{color:var(--ww-green); display:inline-flex;}
.ww-score-val{text-align:right; font-variant-numeric:tabular-nums;}
.ww-score .ww-bar{height:7px; background:#E6EEE1;}
.ww-score:not(.is-top) .ww-bar-fill{background:#9DBAA8;}

[data-testid="stProgress"] > div > div > div > div{background-color:var(--ww-green);}

/* Smaller screens */
@media (max-width: 900px){
  .ww-chip-detail{display:none;}
  .block-container{padding:.9rem 1rem !important;}
  .st-key-left_panel{padding:.9rem; min-height:0;}
  .st-key-right_panel{padding:.9rem; min-height:0;}
}
@media (max-width: 640px){
  .ww-header{align-items:flex-start; flex-wrap:wrap;}
  .ww-header-meta{width:100%; padding-left:3.4rem; justify-content:flex-start;}
  .ww-material-count{display:none;}
  .st-key-left_panel{border-radius:4px 4px 14px 14px; padding:.75rem;}
  .st-key-right_panel{padding:.75rem;}
  .ww-score{grid-template-columns:minmax(0,1.5fr) minmax(0,1fr) 3rem; gap:.5rem;}
  .ww-material-en{font-size:1.45rem;}
}
@media (prefers-reduced-motion: reduce){*,*::before,*::after{scroll-behavior:auto !important; transition:none !important; animation:none !important;}}
"""


def css() -> str:
    text = (
        _CSS.replace("__GREEN__", FOREST_GREEN)
        .replace("__SAGE__", SAGE_MIST)
        .replace("__CREAM__", WARM_CREAM)
        .replace("__DEEP__", DEEP_GREEN)
        .replace("__PLUS__", PLUS_DATA_URI)
        .replace("__MAX__", str(MAX_IMAGES))
        .replace("__LIMIT__", str(MAX_FILE_MB))
    )
    # Collapse to one line: blank lines would break Streamlit's markdown HTML block.
    return re.sub(r"\s+", " ", text).strip()


def style_tag() -> str:
    return f"<style>{FONT_IMPORT} {css()}</style>"
