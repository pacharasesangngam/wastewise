"""Page styling: a calm sorting bench with a high-contrast intake dock."""

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
    "family=Bai+Jamjuree:wght@400;500;600;700&family=Prompt:wght@300;400;500;600;700&display=swap');"
)

_PLUS_SVG = (
    "<svg xmlns='http://www.w3.org/2000/svg' width='40' height='40' viewBox='0 0 40 40'>"
    "<circle cx='20' cy='20' r='20' fill='#356B55'/>"
    "<path d='M12 20h16M20 12v16' stroke='#FFFFFF' stroke-width='2.5' stroke-linecap='round'/></svg>"
)
PLUS_DATA_URI = "data:image/svg+xml;utf8," + quote(_PLUS_SVG, safe="")

_CSS = """
:root{--ww-green:__GREEN__;--ww-sage:__SAGE__;--ww-cream:__CREAM__;--ww-deep:__DEEP__;--ww-accent:#D49A4F;--ww-muted:#617168;--ww-border:#D8E1D9;--ww-surface:#FFFFFF;--ww-radius:12px;--ww-amber:#BD762F;}
html,body,.stApp,.stApp *:not([data-testid="stIconMaterial"]):not(svg):not(path){font-family:'Prompt',system-ui,-apple-system,'Segoe UI',sans-serif;}
[data-testid="stIconMaterial"]{font-family:'Material Symbols Rounded','Material Symbols Outlined' !important;}
.stApp{background:var(--ww-cream);color:var(--ww-deep);}
header[data-testid="stHeader"],[data-testid="stToolbar"],[data-testid="stDecoration"],footer,#MainMenu{display:none !important;}
.block-container{padding:1.5rem 2.25rem 2rem !important;max-width:1320px;}

/* A spare masthead, followed by one unmistakable promise. */
.ww-page-head{margin:0 0 1.5rem;}
.ww-header{display:flex;align-items:center;justify-content:space-between;padding:.15rem 0 .8rem;border-bottom:1px solid var(--ww-border);}
.ww-brand{display:flex;align-items:center;gap:.65rem;}
.ww-logo{display:grid;place-items:center;width:38px;height:38px;border-radius:10px 10px 10px 3px;background:var(--ww-green);color:#fff;}
.ww-title,.ww-brand-name{font-size:1.05rem;font-weight:700;letter-spacing:-.025em;color:var(--ww-deep);}
.ww-chip{display:inline-flex;align-items:center;gap:.45rem;padding:.38rem .72rem;border-radius:999px;font-size:.77rem;line-height:1.25;}
.ww-chip-demo{background:#F5E9BF;color:#57451A;border:1px solid #E2CF8C;}
.ww-chip-live{background:#E5ECE2;color:var(--ww-deep);}
.ww-live-dot{width:8px;height:8px;border-radius:50%;background:#53885D;}
.ww-hero{display:flex;align-items:flex-end;justify-content:space-between;gap:2rem;padding:1.35rem 0 0;}
.ww-hero h1{margin:0;font-family:'Bai Jamjuree','Prompt',sans-serif;font-size:clamp(2.15rem,4.1vw,3.4rem);font-weight:600;letter-spacing:-.045em;line-height:.98;color:var(--ww-deep);}
.ww-hero p{max-width:24rem;margin:0 0 .3rem;color:#5E7065;font-size:.94rem;line-height:1.55;}
.ww-hero-th{display:block;margin-top:.25rem;color:#65766B;font-size:.82rem;}

/* The green rule identifies intake; the result surface stays quiet and clear. */
.st-key-left_panel{gap:.85rem !important;padding:1.25rem 1.25rem 1.35rem;border:1px solid var(--ww-border);border-top:4px solid var(--ww-green);border-radius:12px 12px 18px 12px;background:#fff;color:var(--ww-deep);}
.st-key-right_panel{padding:1.15rem 1.2rem 1.2rem;gap:1rem !important;border:1px solid var(--ww-border);border-top:4px solid #A7BCAF;border-radius:12px 12px 18px 12px;background:var(--ww-surface);}
.ww-section-head{margin:0 0 .8rem;}
.ww-section-title{font-family:'Bai Jamjuree','Prompt',sans-serif;font-size:1.32rem;font-weight:600;letter-spacing:-.02em;color:var(--ww-deep);}
.ww-section-sub{font-size:.82rem;color:var(--ww-muted);margin-top:.08rem;}
.st-key-left_panel .ww-section-title{color:var(--ww-deep);}
.st-key-left_panel .ww-section-sub{color:var(--ww-muted);}

/* Upload dropzone and image queue */
.st-key-upload_area_grid{padding:.8rem !important;border:1px solid var(--ww-border) !important;border-radius:var(--ww-radius) !important;background:#F7F9F6;}
.st-key-upload_area_grid > div:first-child{gap:.8rem;}
.st-key-upload_area_grid [data-testid="stHorizontalBlock"]{margin-bottom:.55rem;}
.st-key-upload_area_empty{padding:0 !important;border:0 !important;background:transparent !important;}
[data-testid="stFileUploader"]>label{display:none;}
[data-testid="stFileUploaderDropzone"]{position:relative;display:flex;flex-direction:column;align-items:center;justify-content:center;gap:.45rem;min-height:148px;padding:1rem;text-align:center;border:1px dashed #91A99A;border-radius:var(--ww-radius);background:#F1F5F1;transition:background .16s ease,border-color .16s ease;}
[data-testid="stFileUploaderDropzone"]:hover{background:#EAF1EB;border-color:var(--ww-green);}
[data-testid="stFileUploaderDropzone"]::before{content:"";display:block;flex:0 0 40px;width:40px;height:40px;margin:0 auto;background:url("__PLUS__") center/contain no-repeat;}
[data-testid="stFileUploaderDropzoneInstructions"]{display:flex !important;flex-direction:column;align-items:center;gap:.12rem;}
[data-testid="stFileUploaderDropzoneInstructions"]>*:not(button){display:none !important;}
[data-testid="stFileUploaderDropzoneInstructions"]::before{content:"Choose up to __MAX__ photos";font-weight:600;font-size:.98rem;color:var(--ww-deep);}
[data-testid="stFileUploaderDropzoneInstructions"]::after{content:"JPG or PNG · up to __LIMIT__MB each";font-size:.76rem;color:var(--ww-muted);}
[data-testid="stFileUploaderDropzone"] button{position:static;width:auto;height:auto;opacity:1;cursor:pointer;z-index:auto;border:1px solid #9BAF9F;border-radius:7px;background:#fff;color:var(--ww-deep);font-size:.82rem;font-weight:600;}
[data-testid="stFileUploaderDropzone"] button:hover{border-color:var(--ww-green);background:#E4ECE5;color:var(--ww-deep);}
[data-testid="stFileUploaderDropzone"]:has(button:disabled){opacity:.55;border-color:#BFCBC0;cursor:not-allowed;}
[data-testid="stFileUploaderDropzone"]:has(button:disabled) button{cursor:not-allowed;}
[data-testid="stFileUploaderFile"]{font-size:.78rem;color:var(--ww-deep);}
.ww-count{font-size:.78rem;color:var(--ww-muted);font-weight:500;margin-top:.05rem;}
[class*="st-key-thumb_card_"]{position:relative;min-width:0;padding-bottom:.15rem;}
.ww-thumb{position:relative;overflow:hidden;border:1px solid var(--ww-border);border-radius:9px;background:#fff;}
.ww-thumb img{display:block;width:100%;aspect-ratio:1/1;object-fit:cover;}
.ww-thumb-name{overflow:hidden;padding:.3rem .4rem .35rem;text-overflow:ellipsis;white-space:nowrap;color:var(--ww-deep);font-size:.7rem;}
[class*="st-key-rm_"]{position:absolute;top:.35rem;right:.35rem;z-index:3;}
[class*="st-key-rm_"] button{width:1.5rem;min-height:1.5rem;padding:0;border:1px solid rgba(255,255,255,.9);border-radius:999px;background:rgba(24,39,32,.84);color:#fff;font-size:.65rem;}
[class*="st-key-rm_"] button:hover{background:var(--ww-accent);color:var(--ww-deep);}
.st-key-add_image_tile{position:relative;min-width:0;aspect-ratio:1/1;overflow:hidden;border:1px dashed #91A99A;border-radius:9px;background:#F1F5F1;}
.st-key-add_image_tile [data-testid="stFileUploader"]{height:100%;}
.st-key-add_image_tile [data-testid="stFileUploaderDropzone"]{height:100%;min-height:0;padding:0;border:0;border-radius:0;background:transparent;}
.st-key-add_image_tile [data-testid="stFileUploaderDropzone"]::before{width:38px;height:38px;flex-basis:38px;}
.st-key-add_image_tile [data-testid="stFileUploaderDropzoneInstructions"]{display:none !important;}
.st-key-add_image_tile [data-testid="stFileUploaderDropzone"] button{position:absolute;inset:0;width:100%;height:100%;opacity:0;border:0;}
.st-key-upload_area_empty [data-testid="stFileUploaderDropzone"]{min-height:142px;padding:1rem;}
.st-key-upload_area_empty [data-testid="stFileUploaderDropzone"]::before{width:40px;height:40px;flex-basis:40px;}
.st-key-upload_area_empty [data-testid="stFileUploaderDropzoneInstructions"]::before{content:"Choose up to __MAX__ photos";font-size:.98rem;}
.st-key-upload_area_empty [data-testid="stFileUploaderDropzoneInstructions"]::after{content:"JPG or PNG · up to __LIMIT__MB each";display:block;font-size:.76rem;}

/* Notices, camera and primary action */
.ww-notices{display:flex;flex-direction:column;gap:.35rem;}
.st-key-notice_bar{margin-bottom:.75rem;padding:.55rem .8rem;border:1px solid #E2CF8C;border-radius:8px;background:#F5E9BF;}
.st-key-notice_bar [data-testid="stHorizontalBlock"]{align-items:center;gap:0 !important;}
.st-key-notice_bar [data-testid="stColumn"]{min-height:0 !important;padding:0 !important;}
.st-key-notice_bar [data-testid="stMarkdown"],.st-key-notice_bar [data-testid="stMarkdownContainer"],.st-key-notice_bar [data-testid="stMarkdownContainer"]>div{margin:0 !important;padding:0 !important;}
.st-key-notice_bar .ww-notice{display:flex;align-items:center;gap:.45rem;min-height:1.8rem;font-size:.8rem;color:#57451A;}
.st-key-notice_bar [class*="st-key-dismiss_notices"] button{width:1.8rem;height:1.8rem;min-height:1.8rem;padding:0;border:0;background:transparent;color:#57451A;}
.st-key-classify_btn{width:100%;margin-top:.05rem;}
[data-testid="stElementContainer"]:has(.st-key-classify_btn){width:100% !important;}
.st-key-classify_btn [data-testid="stButton"],.st-key-classify_btn [data-testid="stButton"]>button{width:100% !important;}
[class*="st-key-classify_btn"] button{width:100%;min-height:3.1rem;border:0;border-radius:8px;background:var(--ww-accent);color:var(--ww-deep);font-size:1rem;font-weight:700;letter-spacing:.005em;}
[class*="st-key-classify_btn"] button:hover:not(:disabled){background:#E0AD68;color:var(--ww-deep);}
[class*="st-key-classify_btn"] button:disabled{background:#E0E6E0;color:#65736A;opacity:1;}
[data-testid="stExpander"] details{border:1px solid var(--ww-border) !important;border-radius:9px !important;background:#fff;}
[data-testid="stExpander"] summary{border-radius:9px;color:var(--ww-deep);background:transparent !important;font-size:.88rem;font-weight:500;}
[data-testid="stExpander"] summary:hover{background:#F1F5F1 !important;color:var(--ww-deep);}
[data-testid="stExpander"] svg{color:var(--ww-green);}
[data-testid="stCameraInput"]{padding:.35rem 0 .1rem;}
[data-testid="stCameraInput"] label{color:var(--ww-deep) !important;}
[data-testid="stCameraInput"] video,[data-testid="stCameraInput"] img{border-radius:7px;}
[data-testid="stCameraInputButton"]{width:100%;border:1px solid var(--ww-green) !important;border-radius:7px !important;background:var(--ww-green) !important;color:#fff !important;font-weight:700 !important;}
[data-testid="stCameraInputButton"]:hover{background:#285740 !important;}
[class*="st-key-webcam_toggle"] button{width:100%;min-height:2.7rem;border:1px solid #91A99A;border-radius:8px;background:#fff;color:var(--ww-deep);font-weight:600;}
[class*="st-key-webcam_toggle"] button:hover{border-color:var(--ww-green);background:#EAF1EB;color:var(--ww-deep);}
.st-key-classify_btn button:focus-visible,[data-testid="stFileUploaderDropzone"] button:focus-visible,[class*="st-key-rm_"] button:focus-visible,[class*="st-key-dismiss_notices"] button:focus-visible,[class*="st-key-webcam_toggle"] button:focus-visible{outline:3px solid var(--ww-amber) !important;outline-offset:3px;}

/* Results states and model output */
.ww-empty-state{display:grid;grid-template-columns:minmax(170px,.8fr) minmax(280px,1.2fr);align-items:center;gap:1.25rem;padding:1.25rem 0;border-top:1px solid var(--ww-border);border-bottom:1px solid var(--ww-border);background:var(--ww-surface);}
.ww-empty-copy{padding:.5rem .4rem;}
.ww-state-icon{display:grid;place-items:center;width:48px;height:48px;margin-bottom:.85rem;border-radius:10px 10px 10px 3px;background:var(--ww-sage);color:var(--ww-green);}
.ww-state-title{font-family:'Bai Jamjuree','Prompt',sans-serif;font-size:1.45rem;font-weight:600;letter-spacing:-.025em;line-height:1.1;}
.ww-state-sub{max-width:26rem;margin-top:.4rem;color:#64756A;font-size:.88rem;line-height:1.5;}
.ww-material-key{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:.45rem;}
.ww-material-tile{display:flex;align-items:center;gap:.35rem;min-width:0;padding:.62rem .4rem;border-left:3px solid var(--material);background:#F0F3ED;}
.ww-material-tile-icon{display:grid;place-items:center;flex:none;width:24px;height:28px;color:var(--material);}
.ww-material-tile b,.ww-material-tile small{display:block;overflow:hidden;text-overflow:ellipsis;white-space:nowrap;}
.ww-material-tile b{font-size:.72rem;font-weight:600;color:var(--ww-deep);}
.ww-material-tile small{margin-top:.05rem;color:#748278;font-size:.68rem;}
.ww-state-error{padding:1.25rem;border:1px solid #DDAAA0;border-radius:8px;background:#FBEEEB;}
.ww-state-error .ww-state-title{color:#783F36;}
.ww-state-error .ww-state-icon{background:#EAC6BE;color:#783F36;}
.stTabs [data-baseweb="tab-list"]{gap:.35rem;border-bottom:1px solid var(--ww-border);}
.stTabs [data-baseweb="tab"]{height:2.55rem;padding:0 .9rem;color:#64756A;font-weight:500;}
.stTabs [aria-selected="true"]{color:var(--ww-deep) !important;font-weight:600;}
.stTabs [data-baseweb="tab-highlight"]{background-color:var(--ww-deep) !important;}
.stTabs [data-baseweb="tab-border"]{display:none;}
[data-testid="stImage"] img{border-radius:4px;}
.ww-result{display:flex;flex-direction:column;gap:.78rem;}
.ww-result .ww-chip{align-self:flex-start;}
.ww-kicker{color:#69796F;font-size:.7rem;font-weight:600;letter-spacing:.035em;}
.ww-kicker-light{color:rgba(255,255,255,.86);}
.ww-material{display:flex;align-items:center;flex-wrap:wrap;gap:.55rem;margin-top:-.35rem;}
.ww-material-icon{display:grid;place-items:center;width:42px;height:42px;background:#E4EAE0;color:var(--ww-deep);}
.ww-material-en{font-family:'Bai Jamjuree','Prompt',sans-serif;font-size:1.8rem;font-weight:600;letter-spacing:-.025em;line-height:1.1;}
.ww-material-th{color:#65766B;font-size:1.1rem;font-weight:500;}
.ww-conf-row{display:flex;justify-content:space-between;margin-bottom:.3rem;font-size:.86rem;}
.ww-conf-row b{color:var(--ww-deep);}
.ww-bar{height:7px;overflow:hidden;border-radius:999px;background:#E4EAE0;}
.ww-bar-fill{height:100%;border-radius:999px;background:#477B5D;}
.ww-fine{margin-top:.3rem;color:#758379;font-size:.73rem;}
.ww-bin{display:flex;align-items:center;gap:.9rem;padding:.9rem 1.1rem;border-radius:4px 12px 4px 4px;background:var(--accent,var(--ww-green));color:#fff;}
.ww-bin-icon{display:grid;place-items:center;flex:none;width:50px;height:50px;background:rgba(255,255,255,.18);}
.ww-bin-name{font-size:1.18rem;font-weight:700;line-height:1.2;}
.ww-bin-th{font-size:.9rem;opacity:.92;}
.ww-instr{font-size:.91rem;line-height:1.55;}
.ww-instr-th{margin-top:.18rem;color:#65766B;}
.ww-scores{display:flex;flex-direction:column;gap:.35rem;}
.ww-score{display:grid;grid-template-columns:minmax(170px,1.6fr) 2fr 3.6rem;align-items:center;gap:.7rem;padding:.35rem .5rem;font-size:.84rem;}
.ww-score.is-top{background:#E8EEE5;font-weight:600;}
.ww-score-name{display:flex;align-items:center;flex-wrap:wrap;column-gap:.35rem;}
.ww-score-th{color:#748278;font-size:.78rem;font-weight:400;white-space:nowrap;}
.ww-score-check{display:inline-flex;color:#477B5D;}
.ww-score-val{text-align:right;font-variant-numeric:tabular-nums;}
.ww-score .ww-bar{height:6px;background:#E0E7DE;}
.ww-score:not(.is-top) .ww-bar-fill{background:#9BAC9C;}
[data-testid="stProgress"]>div>div>div>div{background-color:var(--ww-green);}

@media(max-width:1000px){.block-container{padding:1.2rem 1.25rem 1.5rem !important;}.ww-hero{align-items:flex-start;flex-direction:column;gap:.6rem;}.ww-hero p{max-width:34rem;}.st-key-left_panel{min-height:0;}.st-key-right_panel{min-height:0;padding-left:.3rem;}}
@media(max-width:640px){.block-container{padding:.9rem .85rem 1.2rem !important;}.ww-page-head{margin-bottom:1rem;}.ww-header{padding-bottom:.65rem;}.ww-hero{padding-top:1.1rem;}.ww-hero h1{font-size:2.35rem;}.ww-hero p{font-size:.87rem;}.st-key-left_panel{padding:1rem;border-radius:12px 12px 16px 12px;}.st-key-right_panel{padding:.7rem .75rem;}.ww-empty-state{grid-template-columns:1fr;gap:.9rem;padding:1rem 0;}.ww-material-key{grid-template-columns:repeat(2,minmax(0,1fr));}.ww-score{grid-template-columns:minmax(0,1.4fr) minmax(0,1fr) 3rem;gap:.45rem;}.ww-material-en{font-size:1.5rem;}}
@media(prefers-reduced-motion:reduce){*,*::before,*::after{scroll-behavior:auto !important;transition:none !important;animation:none !important;}}
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
    return re.sub(r"\s+", " ", text).strip()


def style_tag() -> str:
    return f"<style>{FONT_IMPORT} {css()}</style>"
