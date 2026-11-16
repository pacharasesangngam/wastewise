"""Image validation and preview preparation (no Streamlit dependency)."""

from __future__ import annotations

import base64
import io
import uuid
from dataclasses import dataclass

from PIL import Image, ImageOps, UnidentifiedImageError

from .config import ALLOWED_EXTENSIONS, MAX_FILE_BYTES, MAX_FILE_MB

PREVIEW_MAX_PX = 1200
THUMB_PX = 240


class ImageRejected(ValueError):
    """The file cannot be accepted; the message is safe to show to the user."""


@dataclass(frozen=True)
class SelectedImage:
    id: str  # stable identifier; never reused, never position-based
    name: str
    data: bytes  # original bytes, kept for the classifier
    preview: bytes  # JPEG, max 1200px, for the results panel
    thumb_b64: str  # base64 JPEG square thumbnail for the left panel
    size: int


def _flatten(im: Image.Image) -> Image.Image:
    """Return an RGB image, compositing transparency onto white."""
    if im.mode in ("RGBA", "LA") or (im.mode == "P" and "transparency" in im.info):
        rgba = im.convert("RGBA")
        bg = Image.new("RGB", rgba.size, (255, 255, 255))
        bg.paste(rgba, mask=rgba.getchannel("A"))
        return bg
    return im.convert("RGB")


def _jpeg(im: Image.Image, quality: int) -> bytes:
    buf = io.BytesIO()
    im.save(buf, format="JPEG", quality=quality)
    return buf.getvalue()


def prepare_image(name: str, data: bytes) -> SelectedImage:
    ext = name.rsplit(".", 1)[-1].lower() if "." in name else ""
    if ext not in ALLOWED_EXTENSIONS:
        raise ImageRejected("unsupported file type")
    if not data:
        raise ImageRejected("file is empty")
    if len(data) > MAX_FILE_BYTES:
        raise ImageRejected(f"larger than {MAX_FILE_MB}MB")
    try:
        with Image.open(io.BytesIO(data)) as probe:
            probe.verify()
        with Image.open(io.BytesIO(data)) as im:
            im = _flatten(ImageOps.exif_transpose(im))
            preview = im.copy()
            preview.thumbnail((PREVIEW_MAX_PX, PREVIEW_MAX_PX))
            thumb = ImageOps.fit(im, (THUMB_PX, THUMB_PX))
    except (UnidentifiedImageError, OSError, SyntaxError, Image.DecompressionBombError):
        raise ImageRejected("not a readable image") from None

    return SelectedImage(
        id=uuid.uuid4().hex[:12],
        name=name,
        data=data,
        preview=_jpeg(preview, 85),
        thumb_b64=base64.b64encode(_jpeg(thumb, 80)).decode("ascii"),
        size=len(data),
    )
