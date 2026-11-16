"""Class labels and disposal guidance shown in the results UI.

!! PLACEHOLDER CONTENT !!
This mapping drives presentation only. It is NOT part of the AI inference and
must be reviewed against local waste-management rules before real use.
Bin names and accent colours are UI conventions, not universal standards:
bin systems, colours and accepted materials differ by city and country.

To update guidance, edit the entries in ``GUIDANCE`` below; nothing else in the
code base needs to change.
"""

from __future__ import annotations

from dataclasses import dataclass

from .config import CLASS_LABELS


@dataclass(frozen=True)
class ClassGuidance:
    key: str
    name_en: str
    name_th: str
    material_icon: str  # icon name in wastewise/ui/icons.py
    bin_en: str
    bin_th: str
    bin_icon: str  # icon name in wastewise/ui/icons.py
    accent: str  # UI accent only — not a claim about real bin colours
    instructions_en: str
    instructions_th: str


@dataclass(frozen=True)
class WasteBin:
    key: str
    name_en: str
    name_th: str
    color: str
    icon: str


BIN_TYPES: dict[str, WasteBin] = {
    "recyclable": WasteBin("recyclable", "Recyclable waste bin", "ถังขยะรีไซเคิล", "#D4A72C", "recycle"),
    "wet": WasteBin("wet", "Wet waste bin", "ถังขยะเปียก", "#397A54", "recycle"),
    "general": WasteBin("general", "General waste bin", "ถังขยะทั่วไป", "#2F6F9F", "trash"),
    "hazardous": WasteBin("hazardous", "Hazardous waste bin", "ถังขยะอันตราย", "#B83A3A", "alert-circle"),
}

CLASS_TO_BIN: dict[str, str] = {
    "cardboard": "recyclable",
    "glass": "recyclable",
    "metal": "recyclable",
    "paper": "recyclable",
    "plastic": "recyclable",
    "trash": "general",
}

_RECYCLABLE = dict(
    bin_en=BIN_TYPES["recyclable"].name_en,
    bin_th=BIN_TYPES["recyclable"].name_th,
    bin_icon=BIN_TYPES["recyclable"].icon,
    accent=BIN_TYPES["recyclable"].color,
)
_GENERAL = dict(
    bin_en=BIN_TYPES["general"].name_en,
    bin_th=BIN_TYPES["general"].name_th,
    bin_icon=BIN_TYPES["general"].icon,
    accent=BIN_TYPES["general"].color,
)

GUIDANCE: dict[str, ClassGuidance] = {
    "cardboard": ClassGuidance(
        key="cardboard",
        name_en="Cardboard",
        name_th="กล่องกระดาษ",
        material_icon="package",
        instructions_en="Flatten the box and keep it dry. Remove tape and food residue if you can.",
        instructions_th="พับกล่องให้แบนและเก็บให้แห้ง แกะเทปและเศษอาหารออกถ้าทำได้",
        **_RECYCLABLE,
    ),
    "glass": ClassGuidance(
        key="glass",
        name_en="Glass",
        name_th="แก้ว",
        material_icon="wine",
        instructions_en="Empty and rinse. Wrap broken glass safely before disposing of it.",
        instructions_th="เทของเหลวออกและล้างให้สะอาด ห่อเศษแก้วแตกให้มิดชิดก่อนทิ้ง",
        **_RECYCLABLE,
    ),
    "metal": ClassGuidance(
        key="metal",
        name_en="Metal",
        name_th="โลหะ",
        material_icon="cylinder",
        instructions_en="Empty and rinse cans and tins. Flatten them if it is safe to do so.",
        instructions_th="เทของเหลวออกและล้างกระป๋อง บีบให้แบนถ้าปลอดภัย",
        **_RECYCLABLE,
    ),
    "paper": ClassGuidance(
        key="paper",
        name_en="Paper",
        name_th="กระดาษ",
        material_icon="file-text",
        instructions_en="Keep it clean and dry. Greasy or heavily soiled paper may not be accepted.",
        instructions_th="เก็บให้สะอาดและแห้ง กระดาษที่เปื้อนน้ำมันหรืออาหารมากอาจรีไซเคิลไม่ได้",
        **_RECYCLABLE,
    ),
    "plastic": ClassGuidance(
        key="plastic",
        name_en="Plastic",
        name_th="พลาสติก",
        material_icon="cup-soda",
        instructions_en="Empty, rinse and dry. Check which plastic types your local service accepts.",
        instructions_th="เทของเหลวออก ล้างและผึ่งให้แห้ง ตรวจสอบประเภทพลาสติกที่รับรีไซเคิลในพื้นที่ของคุณ",
        **_RECYCLABLE,
    ),
    "trash": ClassGuidance(
        key="trash",
        name_en="General trash",
        name_th="ขยะทั่วไป",
        material_icon="trash",
        instructions_en="Items that cannot be recycled or are heavily soiled go here. Check for special collection rules.",
        instructions_th="ของที่รีไซเคิลไม่ได้หรือเปื้อนมากให้ทิ้งที่นี่ ตรวจสอบว่ามีการเก็บแยกเป็นพิเศษหรือไม่",
        **_GENERAL,
    ),
}

assert tuple(GUIDANCE) == CLASS_LABELS, "GUIDANCE must cover exactly CLASS_LABELS, in order"


def get_guidance(label: str) -> ClassGuidance:
    """Return guidance for a class label (KeyError for unknown labels)."""
    return GUIDANCE[label]
