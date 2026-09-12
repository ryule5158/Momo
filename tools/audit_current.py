from __future__ import annotations

import hashlib
import json
from pathlib import Path
from xml.etree import ElementTree as ET


ROOT = Path(__file__).resolve().parents[1]
SVG = ROOT / "current" / "svg" / "MOMO_R166_REQ146_PANEL.svg"
AI = ROOT / "illustrator" / "MOMO_R166_REQ146_PANEL.ai"
PNG = ROOT / "verification" / "MOMO_R166_REQ146_AI_EXPORT.png"
PDF = ROOT / "verification" / "MOMO_R166_REQ146_AI_EXPORT.pdf"
EXPECTED_SVG_SHA256 = "679f2137d3d8e626e4cc08ec8788a06e4362b5139e525aef3b2e3195598b673f"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


root = ET.parse(SVG).getroot()
checks = {
    "svg_exists": SVG.is_file(),
    "svg_dimensions": (root.get("width"), root.get("height"), root.get("viewBox"))
    == ("71.12mm", "128.5mm", "0 0 711.2 1285"),
    "svg_sha256": sha256(SVG) == EXPECTED_SVG_SHA256,
    "ai_pdf_compatible_header": AI.read_bytes().startswith(b"%PDF-"),
    "ai_nonempty": AI.stat().st_size > 100_000,
    "png_nonempty": PNG.stat().st_size > 10_000,
    "pdf_header": PDF.read_bytes().startswith(b"%PDF-"),
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
    "illustrator_live_readback": {
        "version": "30.3.0",
        "artboard_pt": [201.600006103516, 364.251953125],
        "layers": ["OFFICIAL_BOTTOM_LOCKUP_RASTER", "MOMO_PANEL_VISIBLE_VECTOR"],
        "paths": 238,
        "compound_paths": 8,
        "groups": 47,
        "text_frames": 22,
        "raster_items": 1,
        "placed_items": 0,
    },
}
out = ROOT / "verification" / "CURRENT_BASELINE_AUDIT.json"
out.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
print(report["status"], len(checks), "checks", out)
raise SystemExit(0 if report["status"] == "PASS" else 1)
