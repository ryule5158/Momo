from __future__ import annotations

import hashlib
import json
from pathlib import Path
from xml.etree import ElementTree as ET
import math
import numpy as np
from PIL import Image


ROOT = Path(__file__).resolve().parents[1]
SVG = ROOT / "current" / "svg" / "MOMO_R166_REQ146_PANEL.svg"
AI = ROOT / "illustrator" / "MOMO_R166_REQ146_PANEL.ai"
PNG = ROOT / "verification" / "MOMO_R166_REQ146_AI_EXPORT.png"
PDF = ROOT / "verification" / "MOMO_R166_REQ146_AI_EXPORT.pdf"
EXPECTED_SVG_SHA256 = "fd4cf737c08229c734d99ee20ac1dc574023b848899b6895b6fae7874658527d"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


root = ET.parse(SVG).getroot()
live_path = ROOT / 'verification/REQ156_AI_LIVE_READBACK.json'
live = json.loads(live_path.read_text(encoding='utf-8'))
expected = json.loads((ROOT / 'verification/REQ156_LOGO_PATH_DATA.json').read_text(encoding='utf-8'))
actual = {p['name']: p for p in live['logo_paths']}
errors = []
color_match = True
for item in expected:
    for index, subpath in enumerate(item['subpaths']):
        name = item['name'] if len(item['subpaths']) == 1 else item['name'] + '-' + str(index)
        p = actual[name]
        assert len(p['points']) == len(subpath)
        color_match &= p['color'] == [int(item['stroke'][i:i+2],16) for i in (1,3,5)]
        errors.append(abs(p['width'] - item['width']*72/25.4))
        for source_point, native_point in zip(subpath, p['points']):
            for attr in ('a','l','r'):
                target = [live['artboard_pt'][0] + (53.3+source_point[attr][0])*72/25.4,
                          live['artboard_pt'][1] - (1.8+source_point[attr][1])*72/25.4]
                errors.extend(abs(a-b) for a,b in zip(target,native_point[attr]))
before = np.array(Image.open(ROOT/'verification/REQ156_AI_BEFORE_REPLACE.png').convert('RGB'))
after = np.array(Image.open(PNG).convert('RGB'))
assert before.shape == after.shape
delta = np.any(before != after,axis=2)
h,w = delta.shape
logo_region = (math.floor(w*500/711.2), math.floor(h*10/1285), math.ceil(w*650/711.2), math.ceil(h*95/1285))
x0,y0,x1,y1 = logo_region
outside = delta.copy()
outside[y0:y1,x0:x1] = False
pixel_evidence = {'dimensions_px':[w,h], 'changed_pixels':int(delta.sum()), 'changed_pixels_outside_logo':int(outside.sum()), 'excluded_logo_rectangle_px':list(logo_region)}
checks = {
    "svg_exists": SVG.is_file(),
    "svg_dimensions": (root.get("width"), root.get("height"), root.get("viewBox"))
    == ("71.12mm", "128.5mm", "0 0 711.2 1285"),
    "svg_sha256": sha256(SVG) == EXPECTED_SVG_SHA256,
    "ai_pdf_compatible_header": AI.read_bytes().startswith(b"%PDF-"),
    "ai_nonempty": AI.stat().st_size > 100_000,
    "png_nonempty": PNG.stat().st_size > 10_000,
    "pdf_header": PDF.read_bytes().startswith(b"%PDF-"),
    'ai_live_readback_matches_file': live.get('ai_sha256') == sha256(AI),
    'approved_logo_in_svg': any(e.get('id') == 'req156-flow-cat-mark' and e.get('data-status') == 'USER APPROVED 2026-09-12' for e in root.iter()),
    'native_logo_geometry_and_width': max(errors) < 0.00001,
    'native_logo_colors': bool(color_match),
    'new_logo_path_count': len(actual) == 8,
    'old_logo_removed': live['old_logo_groups'] == 0,
    'non_logo_export_pixels_identical': not bool(outside.any()),
    'logo_actually_changed': bool(delta.any()),
    'original_text_and_brand_retained': live['text_frames'] == 22 and live['raster_items'] == 1 and live['placed_items'] == 0,
}
report = {
    "status": "PASS" if all(checks.values()) else "FAIL",
    "checks": checks,
    "files": {
        str(p.relative_to(ROOT)).replace("\\", "/"): {
            "bytes": p.stat().st_size,
            "sha256": sha256(p),
        }
        for p in (SVG, AI, PNG, PDF)
    },
    'illustrator_live_readback': {k:v for k,v in live.items() if k != 'logo_paths'},
    'logo_max_coordinate_or_width_error_pt': max(errors),
    'ai_export_comparison': pixel_evidence,
}
out = ROOT / "verification" / "CURRENT_BASELINE_AUDIT.json"
out.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
print(report["status"], len(checks), "checks", out)
raise SystemExit(0 if report["status"] == "PASS" else 1)
