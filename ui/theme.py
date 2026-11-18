"""Design tokens and responsive styling for the WasteWise screens."""

from __future__ import annotations

import re
from urllib.parse import quote

from ..config import MAX_FILE_MB, MAX_IMAGES

FONT_IMPORT = (
    "@import url('https://fonts.googleapis.com/css2?"
    "family=Bricolage+Grotesque:wght@400;500;600;700&"
    "family=IBM+Plex+Sans+Thai:wght@300;400;500;600;700&display=swap');"
)

_PLUS_SVG = (
    "<svg xmlns='http://www.w3.org/2000/svg' width='56' height='56' viewBox='0 0 56 56'>"
    "<circle cx='28' cy='28' r='28' fill='#F2C230'/>"
    "<path d='M28 18v20M18 28h20' stroke='#14232F' stroke-width='3' stroke-linecap='round'/></svg>"
)
PLUS_DATA_URI = "data:image/svg+xml;utf8," + quote(_PLUS_SVG, safe="")

_CSS = r"""
:root{--ink:#14232F;--body:#45535F;--muted:#B9C8D3;--paper:#EEF2F4;--line:#CBD3D9;--dock:#14232F;--dock-in:#1B2E3D;--gold:#F2C230;--white:#fff;}
html,body,.stApp,.stApp *:not([data-testid="stIconMaterial"]):not(svg):not(path){font-family:'IBM Plex Sans Thai',system-ui,-apple-system,'Segoe UI',sans-serif;}
[data-testid="stIconMaterial"]{font-family:'Material Symbols Rounded','Material Symbols Outlined' !important;}
.stApp{background:var(--paper);color:var(--ink);}
header[data-testid="stHeader"],[data-testid="stToolbar"],[data-testid="stDecoration"],footer,#MainMenu{display:none!important;}
.block-container{width:100%;max-width:1296px;padding:28px 48px 64px!important;}
.ww-page-head{margin:0 0 48px;}.ww-header{display:flex;align-items:center;justify-content:space-between;gap:16px;}
.ww-brand{display:flex;align-items:center;gap:12px;min-width:0;}.ww-logo{display:grid;place-items:center;flex:none;width:44px;height:44px;border-radius:14px;background:var(--ink);color:var(--gold);}.ww-brand-name{font-family:'Bricolage Grotesque',sans-serif;font-size:22px;font-weight:700;letter-spacing:-.01em;color:var(--ink);}
.ww-chip-live{display:flex;align-items:center;gap:8px;padding:8px 14px;border-radius:999px;background:#DCE3E8;color:#2B4558;font-size:14px;font-weight:500;}.ww-live-dot{width:8px;height:8px;border-radius:50%;background:#3F8A55;}
.ww-hero{display:block;padding:0;}.ww-hero h1,.ww-results-title h1{margin:0;font-family:'Bricolage Grotesque',sans-serif;font-weight:700;letter-spacing:-.03em;color:var(--ink);}.ww-hero h1{font-size:clamp(58px,5.3vw,72px);line-height:1.02;}.ww-hero p{max-width:480px;margin:24px 0 0;color:var(--body);font-size:18px;line-height:1.55;}.ww-hero-th{display:block;margin-top:12px;color:var(--body);font-size:16px;line-height:1.5;}
.st-key-left_panel{padding:0!important;border:0!important;background:transparent!important;}.st-key-upload_dock{display:flex;flex-direction:column;gap:16px;padding:28px;border-radius:28px;background:var(--dock);color:var(--paper);}
.ww-dock-header{display:flex;align-items:baseline;justify-content:space-between;gap:12px;flex-wrap:wrap;}.ww-dock-heading{margin:0;color:var(--paper);font-family:'Bricolage Grotesque',sans-serif;font-size:24px;font-weight:700;}.ww-dock-sub{color:var(--muted);font-size:14px;}
.st-key-upload_area_empty,.st-key-upload_area_grid{padding:0!important;border:0!important;background:transparent!important;}.st-key-upload_area_empty [data-testid="stFileUploader"],.st-key-upload_area_grid [data-testid="stFileUploader"]{width:100%;}.st-key-upload_area_grid [data-testid="stFileUploader"]{margin-top:.75rem;}
[data-testid="stFileUploader"]>label{display:none!important;}[data-testid="stFileUploaderDropzone"]{position:relative;display:flex;min-height:218px;flex-direction:column;align-items:center;justify-content:center;gap:10px;padding:36px 20px;border:2px dashed #6B8294;border-radius:20px;background:transparent;text-align:center;}
[data-testid="stFileUploaderDropzone"]::before{content:"";display:block;flex:none;width:56px;height:56px;background:url("__PLUS__") center/contain no-repeat;}
[data-testid="stFileUploaderDropzoneInstructions"]{display:flex!important;flex-direction:column;align-items:center;gap:4px;}.st-key-upload_area_empty [data-testid="stFileUploaderDropzoneInstructions"]>*:not(button),.st-key-upload_area_grid [data-testid="stFileUploaderDropzoneInstructions"]>*:not(button){display:none!important;}
[data-testid="stFileUploaderDropzoneInstructions"]::before{content:"Drop photos here";color:var(--paper);font-size:18px;font-weight:600;}
[data-testid="stFileUploaderDropzoneInstructions"]::after{content:"JPG or PNG, up to __LIMIT__MB each";color:var(--muted);font-size:14px;}
[data-testid="stFileUploaderDropzone"] button{position:static;width:auto;height:44px;min-height:44px;margin-top:6px;padding:0 22px;border:0;border-radius:12px;background:var(--paper);color:var(--ink);font-size:15px;font-weight:600;opacity:1;}
[data-testid="stFileUploaderDropzone"] button:hover{background:#DCE3E8;color:var(--ink);}
.ww-count{margin-bottom:8px;color:var(--muted);font-size:13px;}.st-key-upload_area_grid [data-testid="stHorizontalBlock"]{gap:8px;}.ww-thumb{overflow:hidden;border:1px solid #6B8294;border-radius:10px;background:var(--paper);}.ww-thumb img{display:block;width:100%;aspect-ratio:1;object-fit:cover;}.ww-thumb-name{overflow:hidden;padding:5px 7px;color:var(--ink);font-size:11px;text-overflow:ellipsis;white-space:nowrap;}
.st-key-upload_dock [data-testid="stHorizontalBlock"]{gap:12px!important;}.st-key-webcam_toggle button{width:100%;min-height:52px;border:1.5px solid #6B8294;border-radius:14px;background:transparent;color:var(--paper);font-size:16px;font-weight:500;}.st-key-webcam_toggle button:hover{border-color:#93A9B8;background:#203646;color:#fff;}.st-key-classify_btn button{width:100%;min-height:52px;border:0;border-radius:14px;background:var(--gold);color:var(--ink);font-size:16px;font-weight:600;}.st-key-classify_btn button:hover:not(:disabled){background:#FFD64D;color:var(--ink);}.st-key-classify_btn button:disabled{background:#2C3F4E;color:#9FB2BF;opacity:1;}
.ww-home-support{margin-top:52px;padding-bottom:16px;border-bottom:1px solid var(--line);}.ww-section-title{font-family:'Bricolage Grotesque',sans-serif;font-size:32px;font-weight:700;letter-spacing:-.02em;color:var(--ink);}.ww-section-sub{margin-top:6px;color:var(--body);font-size:15px;}.ww-empty-state{display:block;padding:24px 0 0;border:0;background:transparent;}.ww-empty-copy{display:none;}.ww-material-key{display:grid;grid-template-columns:repeat(6,minmax(0,1fr));gap:16px;}.ww-material-tile{display:flex;min-width:0;min-height:140px;flex-direction:column;justify-content:space-between;gap:14px;padding:20px;border:0;border-radius:4px;background:var(--material);color:#fff;}.ww-material-tile-icon{display:grid;place-items:center;width:30px;height:30px;color:#fff;}.ww-material-tile-icon svg{width:30px;height:30px;}.ww-material-tile b,.ww-material-tile small{display:block;overflow:hidden;text-overflow:ellipsis;white-space:nowrap;}.ww-material-tile b{color:#fff;font-size:16px;font-weight:600;}.ww-material-tile small{margin-top:2px;color:rgba(255,255,255,.88);font-size:14px;}.ww-home-support:after{content:"6 materials we recognise";float:right;margin-top:-46px;color:var(--body);font-size:14px;font-weight:500;}
/* Results: image cards at left and a compact, dark bin summary at right. */
.stApp [data-testid="stHorizontalBlock"]:has(.st-key-new_photos){flex-direction:row-reverse;align-items:center;}.st-key-new_photos button{min-height:44px;padding:0 20px;border:1.5px solid var(--ink);border-radius:12px;background:transparent;color:var(--ink);font-size:15px;font-weight:600;}.ww-results-title{padding:38px 0 28px;}.ww-results-title h1{font-size:56px;line-height:1.05;}.ww-results-title p{margin:12px 0 0;color:var(--body);font-size:17px;}.ww-title-mobile,.ww-count-mobile{display:none;}
.stApp [class*="st-key-result_card_"]{overflow:hidden;margin-bottom:16px;border-radius:10px;background:#fff;}.ww-bin-band{padding:10px 20px;background:var(--material);color:#fff;font-size:16px;font-weight:600;}.stApp [class*="st-key-result_card_"] [data-testid="stHorizontalBlock"]{gap:20px!important;align-items:flex-start;padding:20px;}.stApp [class*="st-key-result_card_"] [data-testid="stColumn"]{min-width:0;}.stApp [class*="st-key-result_card_"] [data-testid="stColumn"]:first-child{flex:0 0 150px!important;width:150px!important;}.stApp [class*="st-key-result_card_"] [data-testid="stColumn"]:last-child{flex:1 1 300px!important;width:auto!important;}.stApp [class*="st-key-result_card_"] [data-testid="stImage"] img{display:block;width:150px;height:150px;border-radius:12px;object-fit:cover;}.ww-result-summary h2{margin:0;font-family:'Bricolage Grotesque',sans-serif;font-size:26px;font-weight:700;line-height:1.2;color:var(--ink);}.ww-result-summary h2 span{display:block;margin-top:3px;font-family:'IBM Plex Sans Thai',sans-serif;font-size:15px;font-weight:400;color:#52606B;}.ww-prep-list{margin:14px 0 0;padding-left:19px;color:#2F3E4A;font-size:15px;line-height:1.4;}.ww-prep-list li{margin:0 0 8px;padding-left:0;}.ww-prep-list small{display:block;color:#52606B;font-size:13px;}.ww-bin-count{display:flex;align-items:center;justify-content:space-between;gap:12px;color:var(--paper);font-size:16px;}.ww-side-title{font-family:'Bricolage Grotesque',sans-serif;font-size:24px;font-weight:700;}.ww-side-th{display:none;}.st-key-bins_summary{position:sticky;top:20px;display:flex;flex-direction:column;gap:18px;padding:28px;border-radius:24px;background:var(--ink);color:var(--paper);}.st-key-bins_summary .ww-bin-count{padding:0;border:0;background:none;}.st-key-bins_summary .ww-bin-count b{color:var(--paper);}.st-key-bins_summary [class*="st-key-add_more"] button,.st-key-bins_summary [class*="st-key-start_over"] button{width:100%;min-height:52px;border-radius:14px;font-size:16px;}.st-key-bins_summary [class*="st-key-add_more"] button{border:0;background:var(--gold);color:var(--ink);font-weight:600;}.st-key-bins_summary [class*="st-key-start_over"] button{border:1.5px solid #6B8294;background:transparent;color:var(--paper);font-weight:500;}.ww-state-error{padding:20px;border:1px solid #DDAAA0;border-radius:10px;background:#FBEEEB;color:#783F36;}
/* The native camera widget remains the capture control. */
.stApp:has(.st-key-camera_frame){background:radial-gradient(circle at 50% 38%,#2B4558,#08121A);color:var(--paper);}.stApp:has(.st-key-camera_frame) .block-container{max-width:1440px;padding:24px 32px 36px!important;}.ww-camera-brand .ww-brand-name{color:var(--paper);}.ww-camera-live{display:flex;align-items:center;justify-content:center;gap:8px;padding:8px 14px;border-radius:999px;background:rgba(0,0,0,.45);color:var(--paper);font-size:13px;font-weight:600;}.ww-camera-live i{width:8px;height:8px;border-radius:50%;background:#FF7A6B;}.st-key-camera_close button{min-height:44px;border:1.5px solid #6B8294;border-radius:12px;background:transparent;color:var(--paper);}.st-key-camera_frame{position:relative;min-height:520px;padding:20px;border-radius:28px;background:radial-gradient(circle at 50% 40%,#2B4558,#0B1721);}.ww-camera-live{position:absolute;z-index:3;top:24px;left:24px;}.ww-camera-prompt{display:flex;position:absolute;z-index:2;inset:35% 8% auto;flex-direction:column;align-items:center;gap:5px;text-align:center;color:var(--paper);pointer-events:none;}.ww-camera-prompt strong{font-size:20px;font-weight:600;}.ww-camera-prompt span{color:var(--muted);font-size:15px;}.st-key-camera_frame [data-testid="stCameraInput"]{position:relative;z-index:1;padding:0;background:transparent;}.st-key-camera_frame [data-testid="stCameraInput"] label{display:none;}.st-key-camera_frame video{width:100%;height:450px;border-radius:14px;object-fit:cover;opacity:.36;}.st-key-camera_frame [data-testid="stCameraInputButton"]{position:absolute;left:50%;bottom:18px;transform:translateX(-50%);width:76px;height:76px;border:4px solid #fff!important;border-radius:50%!important;background:transparent!important;color:transparent!important;font-size:0!important;}.st-key-camera_frame [data-testid="stCameraInputButton"]:after{content:"";display:block;width:100%;height:100%;border-radius:50%;background:#fff;}.ww-captured-title{display:flex;align-items:baseline;justify-content:space-between;gap:8px;margin-bottom:12px;color:var(--paper);}.ww-captured-title strong{font-family:'Bricolage Grotesque',sans-serif;font-size:22px;}.ww-captured-title span,.ww-camera-count{color:var(--muted);font-size:14px;}.st-key-camera_identify button{min-height:52px;border:0;border-radius:14px;background:var(--gold);color:var(--ink);font-weight:600;}.st-key-camera_done{display:none;}.ww-camera-tip{padding:16px;border-radius:16px;background:#1B2E3D;color:var(--muted);font-size:14px;line-height:1.5;}.st-key-camera_frame [data-testid="stImage"] img{border-radius:12px;aspect-ratio:1;object-fit:cover;}
@media(max-width:1000px){.block-container{padding:24px 28px 52px!important;}.ww-material-key{grid-template-columns:repeat(3,minmax(0,1fr));}.ww-material-tile{min-height:125px;}.stApp [class*="st-key-result_card_"] [data-testid="stColumn"]:first-child{flex-basis:128px!important;width:128px!important;}.stApp [class*="st-key-result_card_"] [data-testid="stImage"] img{width:128px;height:128px;}}
@media(max-width:640px){.block-container{max-width:none;padding:20px 20px 28px!important;}.ww-page-head{margin:0 0 20px;}.ww-header{gap:10px;}.ww-logo{width:36px;height:36px;border-radius:11px;}.ww-brand-name{font-size:19px;}.ww-chip-live{padding:6px 12px;font-size:12px;}.stApp [data-testid="stHorizontalBlock"]:has(.st-key-left_panel){flex-direction:column;gap:20px!important;}.stApp [data-testid="stHorizontalBlock"]:has(.st-key-left_panel)>[data-testid="stColumn"]{width:100%!important;flex:1 1 100%!important;}.ww-hero h1{font-size:40px;line-height:1.05;letter-spacing:-.03em;}.ww-hero p{margin-top:10px;font-size:15px;line-height:1.5;}.ww-hero-th{display:inline;margin:0;font-size:15px;}.ww-dock-header{display:none;}.st-key-upload_dock{gap:12px;padding:18px;border-radius:22px;}.st-key-upload_area_empty [data-testid="stFileUploaderDropzone"]{min-height:0;padding:20px 12px;border-radius:16px;gap:6px;}.st-key-upload_area_empty [data-testid="stFileUploaderDropzone"]::before{width:44px;height:44px;}.st-key-upload_area_empty [data-testid="stFileUploaderDropzoneInstructions"]::before{content:"Add up to 5 photos";font-size:16px;}.st-key-upload_area_empty [data-testid="stFileUploaderDropzoneInstructions"]::after{content:"JPG or PNG · เลือกได้ไม่เกิน 5 รูป";font-size:12px;}.st-key-upload_area_empty [data-testid="stFileUploaderDropzone"] button{width:100%;height:48px;margin-top:12px;font-size:15px;}.st-key-upload_dock [data-testid="stHorizontalBlock"]{flex-direction:column;gap:12px!important;}.st-key-webcam_toggle button,.st-key-classify_btn button{min-height:48px;border-radius:12px;font-size:15px;}.ww-home-support{margin-top:20px;padding:0;border:0;}.ww-home-support .ww-section-title,.ww-home-support .ww-section-sub{display:none;}.ww-material-key{grid-template-columns:repeat(2,minmax(0,1fr));gap:10px;}.ww-material-tile{min-height:67px;justify-content:center;gap:0;padding:12px;border-radius:4px;}.ww-material-tile-icon{display:none;}.ww-material-tile b{font-size:14px;}.ww-material-tile small{margin-top:3px;font-size:12px;}.ww-material-metal{--material:#5A666E!important;}.ww-material-paper{--material:#8A6D0F!important;}
.stApp [data-testid="stHorizontalBlock"]:has(.st-key-new_photos){flex-direction:row;align-items:center;}.st-key-new_photos button{width:44px;height:44px;min-height:44px;padding:0;border-radius:50%;font-size:0;}.st-key-new_photos button:after{content:"←";font-size:20px;}.ww-results-model{display:none;}.ww-results-title{padding:20px 0 16px;}.ww-results-title h1{font-size:32px;line-height:1.08;letter-spacing:-.02em;}.ww-title-desktop,.ww-count-desktop{display:none;}.ww-title-mobile,.ww-count-mobile{display:inline;}.ww-results-title p{margin:8px 0 0;font-size:14px;}.stApp [data-testid="stHorizontalBlock"]:has(.st-key-bins_summary){flex-direction:column;gap:0!important;}.stApp [data-testid="stHorizontalBlock"]:has(.st-key-bins_summary)>[data-testid="stColumn"]{width:100%!important;flex:1 1 100%!important;}.stApp [class*="st-key-result_card_"]{margin-bottom:12px;border-radius:8px;}.ww-bin-band{padding:6px 14px;font-size:13px;}.stApp [class*="st-key-result_card_"] [data-testid="stHorizontalBlock"]{gap:12px!important;padding:14px!important;flex-wrap:nowrap!important;}.stApp [class*="st-key-result_card_"] [data-testid="stColumn"]:first-child{flex:0 0 72px!important;width:72px!important;}.stApp [class*="st-key-result_card_"] [data-testid="stColumn"]:last-child{flex:1 1 auto!important;width:auto!important;}.stApp [class*="st-key-result_card_"] [data-testid="stImage"] img{width:72px;height:72px;border-radius:12px;}.ww-result-summary h2{font-size:19px;line-height:1.25;}.ww-result-summary h2 span{display:inline;margin-left:5px;font-size:13px;}.ww-prep-list{display:block;margin:6px 0 0;padding:0;list-style:none;color:#2F3E4A;font-size:13px;line-height:1.4;}.ww-prep-list li{display:inline;margin:0;padding:0;}.ww-prep-list li:not(:last-child):after{content:" · ";}.ww-prep-list small{display:inline;color:inherit;font-size:inherit;}.st-key-bins_summary{position:static;display:block;margin:0;padding:0 0 92px;border-radius:0;background:transparent;color:var(--ink);}.st-key-bins_summary .ww-side-title,.st-key-bins_summary .ww-side-th,.st-key-bins_summary .ww-bin-count,.st-key-bins_summary [class*="st-key-start_over"]{display:none!important;}.st-key-bins_summary [class*="st-key-add_more"]{position:fixed;z-index:100;right:0;bottom:0;left:0;margin:0;padding:16px 20px calc(28px + env(safe-area-inset-bottom));border-top:1px solid var(--line);background:var(--paper);}.st-key-bins_summary [class*="st-key-add_more"] button{min-height:52px;border-radius:14px;background:var(--ink);color:var(--paper);font-size:16px;}
.stApp:has(.st-key-camera_frame) .block-container{min-height:100dvh;max-width:none;padding:24px 20px 20px!important;}.stApp:has(.st-key-camera_frame) [data-testid="stHorizontalBlock"]:has(.ww-camera-brand){display:flex;flex-direction:row;justify-content:space-between;}.ww-camera-brand{display:none;}.stApp:has(.st-key-camera_frame) .st-key-camera_close{position:fixed;z-index:20;top:24px;left:20px;width:44px;}.ww-camera-live{position:fixed;z-index:10;top:24px;left:50%;transform:translateX(-50%);}.st-key-camera_close button{width:44px;height:44px;min-height:44px;padding:0;border:0;border-radius:50%;background:rgba(0,0,0,.45);font-size:0;}.st-key-camera_close button:after{content:"×";font-size:24px;color:var(--paper);}.stApp:has(.st-key-camera_frame) .st-key-camera_frame{min-height:calc(100dvh - 180px);margin-top:30px;padding:0;background:transparent;}.stApp [data-testid="stHorizontalBlock"]:has(.st-key-camera_frame)>[data-testid="stColumn"]{width:100%!important;flex:1 1 100%!important;}.st-key-camera_queue{position:fixed;z-index:6;right:20px;bottom:24px;left:20px;padding:12px 0 0;background:linear-gradient(transparent,rgba(0,0,0,.68));}.st-key-camera_queue .ww-captured-title strong,.st-key-camera_queue .ww-camera-tip,.st-key-camera_queue .st-key-camera_identify{display:none!important;}.st-key-camera_queue [data-testid="stHorizontalBlock"]{display:flex;flex-direction:row!important;justify-content:center;}.st-key-camera_queue [data-testid="stColumn"]{width:44px!important;flex:0 0 44px!important;}.st-key-camera_queue [data-testid="stImage"] img{width:44px;height:44px;border-radius:12px;object-fit:cover;}.ww-camera-count{position:absolute;left:0;bottom:15px;color:var(--muted);font-size:13px;}.stApp:has(.st-key-camera_frame) .st-key-camera_done{display:block;position:absolute;right:0;bottom:0;}.ww-camera-prompt{inset:42% 8% auto;}.ww-camera-prompt strong{font-size:17px;}.ww-camera-prompt span{font-size:13px;}.st-key-camera_frame video{height:calc(100dvh - 280px);opacity:.6;}.st-key-camera_frame [data-testid="stCameraInputButton"]{bottom:20px;width:72px;height:72px;}.stApp:has(.st-key-camera_frame) .ww-captured-title{position:fixed;left:20px;bottom:110px;z-index:4;}.stApp:has(.st-key-camera_frame) .ww-camera-tip,.stApp:has(.st-key-camera_frame) .st-key-camera_identify{display:none!important;}.stApp:has(.st-key-camera_frame) .st-key-camera_done{display:block;position:fixed;z-index:5;right:20px;bottom:36px;}.st-key-camera_done button{width:84px;min-height:44px;border:0;border-radius:12px;background:var(--gold);color:var(--ink);font-weight:600;}.stApp:has(.st-key-camera_frame) .st-key-camera_count{position:fixed;bottom:110px;left:20px;}
}
/* The camera is a full-screen view at every viewport width. Keep the app canvas
   dark to the edges, and prevent Streamlit's default 3:1 columns from squeezing
   the close control and camera preview on narrow embedded browsers. */
.stApp:has(.st-key-camera_frame){min-height:100dvh;background:radial-gradient(circle at 50% 38%,#2B4558,#08121A)!important;}
.stApp:has(.st-key-camera_frame) .block-container{width:100%;max-width:none;min-height:100dvh;padding:24px 20px 20px!important;}
.stApp:has(.st-key-camera_frame) [data-testid="stHorizontalBlock"]:has(.st-key-camera_frame){display:block;}
.stApp:has(.st-key-camera_frame) [data-testid="stHorizontalBlock"]:has(.st-key-camera_frame)>[data-testid="stColumn"]{width:100%!important;flex:1 1 100%!important;}
.stApp:has(.st-key-camera_frame) .st-key-camera_close{position:fixed;z-index:20;top:24px;left:20px;width:44px;}
.stApp:has(.st-key-camera_frame) .st-key-camera_close button{width:44px;height:44px;min-height:44px;padding:0;font-size:0;}
.stApp:has(.st-key-camera_frame) .st-key-camera_frame{min-height:calc(100dvh - 180px);margin-top:30px;padding:0;background:transparent;}
.stApp:has(.st-key-camera_frame) [data-testid="stCameraInput"],.stApp:has(.st-key-camera_frame) [data-testid="stCameraInput"] [class*="st-emotion-cache"]{background-color:transparent!important;}
.stApp:has(.st-key-camera_frame) [data-testid="stCameraInput"] video{opacity:1!important;background:transparent!important;}
.stApp:has(.st-key-camera_frame) .ww-camera-brand{display:none!important;}
.stApp:has(.st-key-camera_frame) .st-key-camera_close{position:fixed;z-index:30;top:20px;left:20px;width:48px;}
.stApp:has(.st-key-camera_frame) .st-key-camera_close button{width:48px;height:48px;min-height:48px;padding:0;border:0;border-radius:50%;background:rgba(0,0,0,.45);font-size:28px!important;line-height:1;color:var(--paper);}
.stApp:has(.st-key-camera_frame) .st-key-camera_close button:after{content:none!important;}
.stApp:has(.st-key-camera_frame) .ww-camera-live{position:fixed;z-index:30;top:22px;left:50%;transform:translateX(-50%);}
.stApp:has(.st-key-camera_frame) .st-key-camera_frame{width:100%;max-width:1100px;min-height:0!important;margin:82px auto 0;}
.stApp:has(.st-key-camera_frame) [data-testid="stCameraInput"]{width:100%;max-width:1000px;margin:0 auto;}
.stApp:has(.st-key-camera_frame) [data-testid="stCameraInput"] video{display:block;width:100%;height:min(58dvh,560px);object-fit:contain;border-radius:14px;}
.stApp:has(.st-key-camera_frame) [data-testid="stCameraInput"] div:has(> img[alt="Snapshot"]){display:flex;align-items:center;justify-content:center;width:min(100%,35vw)!important;max-width:560px;height:clamp(160px,30dvh,320px)!important;max-height:320px;margin:0 auto;overflow:hidden;background:transparent!important;}
.stApp:has(.st-key-camera_frame) [data-testid="stCameraInput"] img[alt="Snapshot"]{width:auto!important;height:auto!important;max-width:100%!important;max-height:100%!important;object-fit:contain!important;opacity:1!important;}
.stApp:has(.st-key-camera_frame) .st-key-camera_frame:has(img[alt="Snapshot"]) [data-testid="stCameraInput"] video{display:none!important;}
.stApp:has(.st-key-camera_frame) .st-key-camera_frame:has(img[alt="Snapshot"]) .ww-camera-prompt{display:none!important;}
.stApp:has(.st-key-camera_frame) [data-testid="stCameraInputButton"]{bottom:18px;}
.stApp:has(.st-key-camera_frame) .st-key-camera_queue .ww-captured-title{display:none!important;}
.stApp:has(.st-key-camera_frame) .st-key-camera_done{position:fixed;z-index:30;right:20px;bottom:24px;width:84px;}
.stApp:has(.st-key-camera_frame) .st-key-camera_done button{width:84px;height:48px;min-height:48px;padding:0;border:0;border-radius:12px;background:var(--gold)!important;color:var(--ink)!important;font-size:16px;font-weight:600;}
.stApp:has(.st-key-camera_frame) .st-key-camera_queue{position:fixed;z-index:6;right:20px;bottom:24px;left:20px;padding:12px 0 0;background:linear-gradient(transparent,rgba(0,0,0,.68));}
.stApp:has(.st-key-camera_frame) .st-key-camera_queue [data-testid="stHorizontalBlock"]{display:flex;flex-direction:row!important;justify-content:center;gap:8px!important;}
.stApp:has(.st-key-camera_frame) .st-key-camera_queue [data-testid="stColumn"]{width:48px!important;flex:0 0 48px!important;}
.stApp:has(.st-key-camera_frame) .st-key-camera_queue [data-testid="stImage"] img{display:block;width:48px!important;height:48px!important;border-radius:10px;object-fit:cover;}
.stApp:has(.st-key-camera_frame) .st-key-camera_queue .ww-captured-title strong,.stApp:has(.st-key-camera_frame) .st-key-camera_queue .ww-camera-tip,.stApp:has(.st-key-camera_frame) .st-key-camera_queue .st-key-camera_identify{display:none!important;}
.stApp:has(.st-key-camera_frame) .st-key-camera_done{display:block;position:fixed;z-index:20;right:20px;bottom:36px;}
.ww-bin-total{display:flex;flex-direction:column;gap:2px;color:var(--muted);font-size:13px;line-height:1.4;}
.ww-bin-row{display:flex;align-items:center;gap:12px;min-height:64px;margin-bottom:10px;padding:10px 14px;border-radius:9px;background:var(--material);color:#fff;}
.ww-bin-icon{display:grid;place-items:center;flex:none;width:40px;height:40px;border-radius:50%;background:rgba(255,255,255,.18);}
.ww-bin-icon svg{width:20px;height:20px;}
.ww-bin-label{display:flex;min-width:0;flex:1;flex-direction:column;line-height:1.25;}
.ww-bin-label b{overflow:hidden;font-size:14px;font-weight:600;text-overflow:ellipsis;white-space:nowrap;}
.ww-bin-label small{margin-top:2px;color:rgba(255,255,255,.86);font-size:12px;}
.ww-bin-row>strong{font-size:22px;font-weight:700;}
.ww-bin-divider{height:1px;margin:2px 0;border-top:1px solid rgba(255,255,255,.14);}
@media(max-width:640px){
  .block-container{padding:16px 16px calc(24px + env(safe-area-inset-bottom))!important;}
  .ww-header{align-items:center;}
  .ww-page-head{margin-bottom:18px;}
  .st-key-upload_area_grid [data-testid="stHorizontalBlock"]{display:flex;flex-wrap:wrap;gap:8px!important;}
  .st-key-upload_area_grid [data-testid="stHorizontalBlock"]>[data-testid="stColumn"]{flex:0 0 calc(50% - 4px)!important;width:calc(50% - 4px)!important;}
  .st-key-upload_dock{padding:16px;border-radius:20px;}
  .st-key-upload_area_empty [data-testid="stFileUploaderDropzone"] button{min-height:48px;}
  .ww-home-support{margin-top:18px;}
  .ww-material-key{gap:8px;}
  .ww-material-tile{min-height:64px;padding:10px;}
  .st-key-bins_summary .ww-bin-total,.st-key-bins_summary .ww-bin-row,.st-key-bins_summary .ww-bin-divider{display:none!important;}
  .stApp [class*="st-key-result_card_"] [data-testid="stHorizontalBlock"]{gap:10px!important;padding:12px!important;}
  .stApp [class*="st-key-result_card_"] [data-testid="stColumn"]:first-child{flex:0 0 76px!important;width:76px!important;}
  .stApp [class*="st-key-result_card_"] [data-testid="stImage"] img{width:76px;height:76px;}
  .stApp:has(.st-key-camera_frame) .block-container{padding:16px 14px calc(20px + env(safe-area-inset-bottom))!important;}
  .stApp:has(.st-key-camera_frame) .st-key-camera_frame{min-height:0;margin-top:30px;}
  .stApp:has(.st-key-camera_frame) [data-testid="stCameraInput"] div:has(> img[alt="Snapshot"]){width:100%!important;max-width:100%;height:clamp(160px,35dvh,300px)!important;max-height:300px;}
  .stApp:has(.st-key-camera_frame) [data-testid="stCameraInput"] video{height:clamp(260px,58dvh,520px);}
  .stApp:has(.st-key-camera_frame) .ww-camera-live{top:16px;}
  .stApp:has(.st-key-camera_frame) .st-key-camera_done{right:14px;bottom:calc(20px + env(safe-area-inset-bottom));}
  .stApp:has(.st-key-camera_frame) .st-key-camera_queue{right:14px;bottom:calc(78px + env(safe-area-inset-bottom));left:14px;}
  .stApp:has(.st-key-camera_frame) .ww-camera-count{bottom:8px;}
}
@media(min-width:641px){
  .ww-results-title{padding:26px 0 20px;}
  .ww-results-title h1{font-size:clamp(36px,3.4vw,46px);line-height:1.08;}
  .ww-results-title p{margin-top:8px;font-size:15px;}
  .stApp [class*="st-key-result_card_"]{margin-bottom:12px;border-radius:12px;}
  .ww-bin-band{padding:9px 16px;font-size:15px;}
  .stApp [class*="st-key-result_card_"] [data-testid="stHorizontalBlock"]{gap:16px!important;padding:16px;}
  .stApp [class*="st-key-result_card_"] [data-testid="stColumn"]:first-child{flex-basis:112px!important;width:112px!important;}
  .stApp [class*="st-key-result_card_"] [data-testid="stImage"] img{width:112px;height:112px;border-radius:10px;}
  .ww-result-summary h2{font-size:22px;}
  .ww-prep-list{margin-top:9px;font-size:14px;}
  .ww-prep-list li{margin-bottom:5px;}
  .ww-prep-list small{font-size:12px;}
  .st-key-bins_summary{gap:14px;padding:22px;border-radius:20px;}
  .ww-side-title{font-size:22px;}
  .st-key-bins_summary [class*="st-key-add_more"] button,.st-key-bins_summary [class*="st-key-start_over"] button{min-height:46px;font-size:15px;}
}
@media(prefers-reduced-motion:reduce){*,*::before,*::after{scroll-behavior:auto!important;transition:none!important;animation:none!important;}}
"""


def css() -> str:
    text = _CSS.replace("__PLUS__", PLUS_DATA_URI).replace("__MAX__", str(MAX_IMAGES)).replace("__LIMIT__", str(MAX_FILE_MB))
    return re.sub(r"\s+", " ", text).strip()


def style_tag() -> str:
    return f"<style>{FONT_IMPORT} {css()}</style>"
