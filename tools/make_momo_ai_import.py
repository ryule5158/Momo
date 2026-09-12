from __future__ import annotations

import copy
import base64
import io
import re
from pathlib import Path
from xml.etree import ElementTree as ET

from PIL import Image


SVG = "http://www.w3.org/2000/svg"
XLINK = "http://www.w3.org/1999/xlink"
ET.register_namespace("", SVG)
ET.register_namespace("xlink", XLINK)

SOURCE = Path(r"C:\Users\LENOVO\Desktop\Momo\current\svg\MOMO_R166_REQ146_PANEL.svg")
TARGET = Path(r"C:\Users\LENOVO\Desktop\Momo\verification\MOMO_VISIBLE_VECTOR_EXPANDED.svg")
BRAND = Path(r"C:\Users\LENOVO\Desktop\Momo\verification\MOMO_OFFICIAL_BOTTOM_LOCKUP.png")


def local(tag: str) -> str:
    return tag.rsplit("}", 1)[-1]


def remove_ids(element: ET.Element) -> None:
    element.attrib.pop("id", None)
    for child in element:
        remove_ids(child)


tree = ET.parse(SOURCE)
root = tree.getroot()

# Extract the one embedded official lockup, applying the SVG color matrix to
# RGB while retaining its alpha channel. It is reinserted as an embedded AI item.
image = next(e for e in root.iter() if local(e.tag) == "image")
href = image.get("href") or image.get(f"{{{XLINK}}}href")
filter_id = re.fullmatch(r"url\(#([^)]+)\)", image.get("filter", "")).group(1)
filter_element = next(e for e in root.iter() if e.get("id") == filter_id)
matrix = next(e for e in filter_element.iter() if local(e.tag) == "feColorMatrix")
values = [float(v) for v in matrix.get("values", "").split()]
rgb = tuple(max(0, min(255, round(values[i] * 255))) for i in (4, 9, 14))
source_image = Image.open(io.BytesIO(base64.b64decode(href.split(",", 1)[1]))).convert("RGBA")
alpha = source_image.getchannel("A")
brand_image = Image.new("RGBA", source_image.size, (*rgb, 255))
brand_image.putalpha(alpha)
BRAND.parent.mkdir(parents=True, exist_ok=True)
brand_image.save(BRAND, format="PNG", optimize=True)

# Inline the compact CSS classes used by the source. Illustrator imports these
# properties more reliably as presentation attributes.
class_styles: dict[str, dict[str, str]] = {}
for style in [e for e in root.iter() if local(e.tag) == "style"]:
    for selector, body in re.findall(r"\.([\w-]+)\s*\{([^}]*)\}", style.text or ""):
        props = class_styles.setdefault(selector, {})
        for declaration in body.split(";"):
            if ":" not in declaration:
                continue
            key, value = declaration.split(":", 1)
            props[key.strip()] = value.strip()

for element in root.iter():
    for cls in element.get("class", "").split():
        for key, value in class_styles.get(cls, {}).items():
            element.attrib.setdefault(key, value)
    element.attrib.pop("class", None)

# Expand <use> references into independent vectors. This preserves the visible
# knob, jack, mounting-hole and light-pipe geometry as editable Illustrator art.
ids = {e.get("id"): e for e in root.iter() if e.get("id")}
expanded = 0
for parent in list(root.iter()):
    for index, child in list(enumerate(list(parent))):
        if local(child.tag) != "use":
            continue
        href = child.get(f"{{{XLINK}}}href") or child.get("href")
        if not href or not href.startswith("#") or href[1:] not in ids:
            continue
        clone = copy.deepcopy(ids[href[1:]])
        remove_ids(clone)
        wrapper = ET.Element(f"{{{SVG}}}g")
        for key, value in child.attrib.items():
            if key not in (f"{{{XLINK}}}href", "href", "x", "y"):
                wrapper.set(key, value)
        x, y = child.get("x", "0"), child.get("y", "0")
        transform = child.get("transform", "")
        if x != "0" or y != "0":
            transform = f"translate({x} {y}) " + transform
        if transform.strip():
            wrapper.set("transform", transform.strip())
        wrapper.append(clone)
        parent.remove(child)
        parent.insert(index, wrapper)
        expanded += 1

removed_hidden = 0
removed_special = 0
for parent in list(root.iter()):
    for child in list(parent):
        compact_style = child.get("style", "").replace(" ", "").lower()
        tag = local(child.tag)
        if "display:none" in compact_style:
            parent.remove(child)
            removed_hidden += 1
        elif tag in {"image", "filter", "style", "metadata"}:
            parent.remove(child)
            removed_special += 1

for element in root.iter():
    element.attrib.pop("filter", None)
    element.attrib.pop("clip-path", None)

TARGET.parent.mkdir(parents=True, exist_ok=True)
tree.write(TARGET, encoding="utf-8", xml_declaration=True)
print(
    f"PASS expanded_use={expanded} removed_hidden={removed_hidden} "
    f"removed_special={removed_special} target={TARGET}"
)
